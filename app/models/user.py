from ..extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Liên kết n-n giữa User và Role
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role', secondary=roles_users, backref='users')

    # Kiểm tra quyền admin
    @property
    def is_admin(self):
        return any(r.name == 'admin' for r in self.roles)

    # Mã hóa mật khẩu
    def set_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password_hash = generate_password_hash(password)

    # Kiểm tra mật khẩu
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Tạo admin mặc định
    @staticmethod
    def create_admin(email, password):
        user = User(username=email, email=email)
        user.set_password(password)

        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.flush()  # đảm bảo có id để gán

        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()
        return user
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.login_view = 'auth.login'
