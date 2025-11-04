from ..extensions import db
from datetime import datetime


class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    code = db.Column(db.String(32), unique=True, nullable=False)
    status = db.Column(db.String(20), default='DRAFT') # DRAFT, SUBMITTED, RECEIVED, CANCELLED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    supplier = db.relationship('Supplier')


class PurchaseOrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Numeric(12,2), nullable=False)
    batch_no = db.Column(db.String(64))
    expiry_date = db.Column(db.Date)

    po = db.relationship('PurchaseOrder', backref='items')
    product = db.relationship('Product')