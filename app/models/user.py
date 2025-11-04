from ..extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role', secondary=roles_users, backref='users')


    @property
    def is_admin(self):
        return any(r.name == 'admin' for r in self.roles)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    @staticmethod
    def create_admin(email, password):
        user = User(email=email)
        user.set_password(password)
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
        user.roles.append(admin_role)
        return user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.login_view = 'auth.login'