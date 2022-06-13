from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(shopper_id):
    return Shopper.query.get(shopper_id)

class Shopper(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable = False)
    carts = db.relationship('Cart', backref='shopper') # <-- this is how to set up a foreign key!!

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Shopper | {self.username} >< email | {self.email}>"

    def check_password(self, password):
        return check_password_hash(self.password, password) 

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopper_id = db.Column(db.Integer, db.ForeignKey('shopper.id'), nullable=False) #references 'shopper' in table
    item = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(8,2), nullable=False)
    quantity = db.Column(db.String(17), nullable=False)
    total = db.Column(db.Numeric(8,2), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Cart | {self.id} >< Shopper | {self.shopper.id} >"

    def update(self, item, price, quantity):
        self.item = item
        self.price = price
        self.quantity = quantity
        self.total = self.price * self.quantity
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
