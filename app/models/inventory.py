from ..extensions import db
from sqlalchemy.orm import validates
from datetime import datetime


class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    batch_no = db.Column(db.String(64))
    expiry_date = db.Column(db.Date)
    quantity = db.Column(db.Integer, default=0)
    unit_cost = db.Column(db.Numeric(12,2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product')
    warehouse = db.relationship('Warehouse')


class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    from_warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    to_warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    batch_no = db.Column(db.String(64))
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Numeric(12,2))
    type = db.Column(db.String(10), nullable=False) # IN, OUT, TRANSFER
    ref = db.Column(db.String(64)) # PO number, SO number, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product')
    from_warehouse = db.relationship('Warehouse', foreign_keys=[from_warehouse_id])
    to_warehouse = db.relationship('Warehouse', foreign_keys=[to_warehouse_id])