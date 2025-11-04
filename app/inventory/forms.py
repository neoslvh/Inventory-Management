from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    barcode = StringField('Barcode')
    unit = StringField('Unit')
    min_stock = IntegerField('Min stock')
    cost_price = DecimalField('Cost price')
    sell_price = DecimalField('Sell price')
    submit = SubmitField('Save')