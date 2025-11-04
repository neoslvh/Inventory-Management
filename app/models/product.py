from ..extensions import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(64), unique=True, nullable=False)
    barcode = db.Column(db.String(64), unique=True)
    unit = db.Column(db.String(20), default='pcs')
    min_stock = db.Column(db.Integer, default=0)
    cost_price = db.Column(db.Numeric(12,2), default=0)
    sell_price = db.Column(db.Numeric(12,2), default=0)