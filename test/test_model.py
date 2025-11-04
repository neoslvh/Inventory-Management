from app.extensions import db
from app.models.product import Product


def test_create_product(app):
    p = Product(name='Test', sku='SKU1')
    db.session.add(p)
    db.session.commit()
    assert p.id is not None