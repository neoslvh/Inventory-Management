from flask import jsonify, request
from flask_restful import reqparse
from ..extensions import db
from ..models.product import Product
from ..models.inventory import InventoryItem
from . import api_bp


@api_bp.get('/products')
def api_products():
    q = request.args.get('q')
    query = Product.query
    if q:
        like = f"%{q}%"
        query = query.filter((Product.name.ilike(like)) | (Product.sku.ilike(like)) | (Product.barcode.ilike(like)))
    items = query.order_by(Product.name).limit(100).all()
    return jsonify([{'id': p.id, 'name': p.name, 'sku': p.sku, 'barcode': p.barcode} for p in items])


@api_bp.get('/stock/<int:product_id>')
def api_stock(product_id):
    total = db.session.query(db.func.coalesce(db.func.sum(InventoryItem.quantity),0)).filter_by(product_id=product_id).scalar()
    return jsonify({'product_id': product_id, 'total': int(total)})