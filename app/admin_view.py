from flask_admin.contrib.sqla import ModelView
from .extensions import admin, db
from .models.user import User, Role
from .models.supplier import Supplier
from .models.warehouse import Warehouse
from .models.product import Product
from .models.inventory import InventoryItem, StockMovement
from .models.purchasing import PurchaseOrder, PurchaseOrderItem


class SecureModelView(ModelView):
    def is_accessible(self):
        from flask_login import current_user
        return current_user.is_authenticated and current_user.is_admin


def register_admin(app):
    admin.add_view(SecureModelView(User, db.session, name="Users", endpoint="admin_user_view"))
    admin.add_view(SecureModelView(Role, db.session, name="Roles", endpoint="admin_role_view"))
    admin.add_view(SecureModelView(Supplier, db.session, name="Suppliers", endpoint="admin_supplier_view"))
    admin.add_view(SecureModelView(Warehouse, db.session, name="Warehouses", endpoint="admin_warehouse_view"))
    admin.add_view(SecureModelView(Product, db.session, name="Products", endpoint="admin_product_view"))
    admin.add_view(SecureModelView(InventoryItem, db.session, name="Inventory", endpoint="admin_inventory_view"))
    admin.add_view(SecureModelView(StockMovement, db.session, name="Movements", endpoint="admin_movement_view"))
    admin.add_view(SecureModelView(PurchaseOrder, db.session, name="Purchase Orders", endpoint="admin_po_view"))
    admin.add_view(SecureModelView(PurchaseOrderItem, db.session, name="PO Items", endpoint="admin_poi_view"))
