from app.extensions import db
from app.models.product import Product


def test_api_products(client):
    db.session.add(Product(name='Milk', sku='MLK'))
    db.session.commit()
    res = client.get('/api/products?q=Milk')
    assert res.status_code == 200
    data = res.get_json()
    assert data and data[0]['name'] == 'Milk'