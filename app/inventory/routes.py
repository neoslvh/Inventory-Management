from flask import render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import login_required
from sqlalchemy import func
from ..extensions import db, socketio
from ..models.product import Product
from ..models.inventory import InventoryItem, StockMovement
from ..models.warehouse import Warehouse
from ..models.purchasing import PurchaseOrder, PurchaseOrderItem
from . import inventory_bp
from .forms import ProductForm
from io import BytesIO
import pandas as pd
from datetime import date


@inventory_bp.route('/')
@login_required
def dashboard():
# Aggregate stock per product
    stock = db.session.query(
        Product.id, Product.name,
        func.coalesce(func.sum(InventoryItem.quantity), 0).label('qty')
        ).join(InventoryItem, InventoryItem.product_id == Product.id, isouter=True)
    stock = stock.group_by(Product.id).order_by(Product.name).all()


    low = db.session.query(Product).join(InventoryItem, isouter=True) \
    .group_by(Product.id) \
    .having(func.coalesce(func.sum(InventoryItem.quantity), 0) < func.coalesce(Product.min_stock, 0)).all()


    # Chart data
    labels = [s.name for s in stock]
    data = [int(s.qty or 0) for s in stock]
    return render_template('./dashboard.html', labels=labels, data=data, low=low)


@inventory_bp.route('/products')
@login_required
def products():
    q = request.args.get('q', '')
    query = Product.query
    if q:
        like = f"%{q}%"
        query = query.filter((Product.name.ilike(like)) | (Product.sku.ilike(like)) | (Product.barcode.ilike(like)))
    items = query.order_by(Product.name).all()
    return render_template('./products.html', items=items, q=q)


@inventory_bp.route('/products/new', methods=['GET','POST'])
@login_required
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        data = form.data.copy()
        data.pop('submit', None)
        data.pop('csrf_token', None)
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        flash('Created', 'success')
        return redirect(url_for('inventory.products'))
    return render_template('./product_form.html', form=form, action='New')


@inventory_bp.route('/products/<int:id>/edit', methods=['GET','POST'])
@login_required
def movements():
    if request.method == 'POST':
        mtype = request.form['type']
        product_id = int(request.form['product_id'])
        qty = int(request.form['quantity'])
        wh_from = request.form.get('from_warehouse_id')
        wh_to = request.form.get('to_warehouse_id')
        batch_no = request.form.get('batch_no')
        unit_cost = request.form.get('unit_cost')


        move = StockMovement(
        type=mtype, product_id=product_id, quantity=qty,
        from_warehouse_id=wh_from or None, to_warehouse_id=wh_to or None,
        batch_no=batch_no or None, unit_cost=unit_cost or None
        )
        db.session.add(move)


        # Simple stock application (FIFO/LIFO can be toggled via query param or config)
        if mtype == 'IN':
            inv = InventoryItem(product_id=product_id, warehouse_id=wh_to, batch_no=batch_no, quantity=qty, unit_cost=unit_cost)
            db.session.add(inv)
        elif mtype == 'OUT':
        # naive FIFO: consume oldest items first
            remaining = qty
            lots = InventoryItem.query.filter_by(product_id=product_id).order_by(InventoryItem.created_at.asc()).all()
            for lot in lots:
                if remaining <= 0:
                    break
                take = min(lot.quantity, remaining)
                lot.quantity -= take
                remaining -= take
        elif mtype == 'TRANSFER':
            remaining = qty
            lots = InventoryItem.query.filter_by(product_id=product_id, warehouse_id=wh_from).order_by(InventoryItem.created_at.asc()).all()
            for lot in lots:
                if remaining <= 0: break
                take = min(lot.quantity, remaining)
                lot.quantity -= take
        # create new lot in destination warehouse with same batch
                db.session.add(InventoryItem(product_id=product_id, warehouse_id=wh_to, batch_no=lot.batch_no, quantity=take, unit_cost=lot.unit_cost))
                remaining -= take


        db.session.commit()
        # from ..extensions import socketio
        # socketio.emit('stock_updated', {'product_id': product_id})
        flash('Movement recorded', 'success')
        return redirect(url_for('inventory.movements'))

    products = Product.query.order_by(Product.name).all()
    warehouses = Warehouse.query.order_by(Warehouse.name).all()
    moves = StockMovement.query.order_by(StockMovement.created_at.desc()).limit(50).all()
    return render_template('./movements.html', products=products, warehouses=warehouses, moves=moves)

@inventory_bp.route('/scan')
@login_required
def scan():
    return render_template('./scan.html')

@inventory_bp.route('/export/inventory.xlsx')
@login_required
def export_inventory():
    q = db.session.query(
    Product.sku, Product.name, InventoryItem.batch_no, InventoryItem.quantity,
    InventoryItem.unit_cost, InventoryItem.expiry_date
    ).join(InventoryItem, InventoryItem.product_id == Product.id, isouter=True)
    df = pd.read_sql(q.statement, db.session.bind)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventory')
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f"inventory_{date.today()}.xlsx")

@inventory_bp.route('/api/low-stock')
@login_required
def low_stock_json():
    res = db.session.execute(
    """
    SELECT p.id, p.name, COALESCE(SUM(i.quantity),0) as qty, p.min_stock
    FROM product p
    LEFT JOIN inventory_item i ON i.product_id = p.id
    GROUP BY p.id
    HAVING COALESCE(SUM(i.quantity),0) < COALESCE(p.min_stock,0)
    """
    ).mappings().all()
    return jsonify([dict(r) for r in res])