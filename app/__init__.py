from flask import Flask, render_template
from .extensions import db, migrate, login_manager, csrf, admin, socketio, cache
from .admin_view import register_admin
from .auth import auth_bp
from .inventory import inventory_bp
from .api import api_bp
from .reports import reports_bp
from .docs.swagger import register_swagger
import os
from .models.user import User, Role



def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    env = os.getenv("FLASK_ENV", "development")
    from config import config_map
    app.config.from_object(config_map.get(env, config_map['development']))

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    cache.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    register_swagger(app)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404


    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return render_template("500.html"), 500


    # Seed an initial admin if missing
    @app.before_request
    def seed_admin():
        db.create_all()
        if not User.query.filter_by(email=os.getenv("ADMIN_EMAIL")).first():
            u = User.create_admin(os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD"))
            db.session.add(u)
            db.session.commit()
    
    register_admin(app)
    admin.init_app(app)
    return app