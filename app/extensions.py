from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_admin import Admin
from flask_socketio import SocketIO
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
admin = Admin(name='Inventory Admin', template_mode='bootstrap4')
socketio = SocketIO()
cache = Cache()
