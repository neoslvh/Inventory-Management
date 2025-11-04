from app import create_app
from app.extensions import db
from flask_migrate import upgrade
from app.extensions import socketio


app = create_app()


if __name__ == "__main__":
# Auto-upgrade db on dev runs
    with app.app_context():
        try:
            upgrade()
        except Exception as e:
            app.logger.warning(f"DB upgrade skipped: {e}")
    socketio.run(app, host="0.0.0.0", port=5000)