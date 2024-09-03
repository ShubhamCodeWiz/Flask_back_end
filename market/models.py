from market import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"item:{self.name}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'barcode': self.barcode,
            'description': self.description,
            'owner': self.owner
        }

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref="owned_user", lazy=True)

    @property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, p):
        self.password_hash = bcrypt.generate_password_hash(p).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'budget': self.budget,
            'items': [item.to_dict() for item in self.items]
        }