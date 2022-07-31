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
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable = False)
    # set up a foreign key relship to cart
    carts = db.relationship('Cart', backref='shopper')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Shopper | {self.username} >< email | {self.email}>"

    # authorization for API
    def get_token(self, expires_in=3600):
        now=datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password) 
    
    @basic_auth.verify_password
    def verify(shopper_email, shopper_password):
        shppoer = Shopper.query.filter_by(email=shopper_email).first()
        if shopper and shopper.check_password(shopper_password):
            return shopper

    @token_auth.verify_token
    def verify(shopper_token):
        shopper = Shopper.query.filter_by(token=shopper_token).first()
        if shopper and shopper.token_expiration > datetime.utcnow():
            return shopper

    def update(self, data):
        for info in data:
            if info in {'email', 'password', 'first_name', 'last_name'}:
                if info == 'password':
                    setattr(self, info, generate_password_hash(data[info]))
                else:
                    setattr(self, info, data[info])
            else:
                return
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict():
        data = {
            'id': self.id,
            'email': self.email, 
            'first_name': self.first_name,
            'last_name': self.last_name
        }
        my_carts = Cart.query.filter(Cart.shopper_id == str(self.id)).first()
        if my_carts: 
            data['carts'] = my_carts.to_dict()
        else:
            data['carts'] = {}
        return data

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopper_id = db.Column(db.Integer, db.ForeignKey('shopper.id'), nullable=False) #references 'shopper' in table
    items = db.relationship('CartItems', backref='items', uselist=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Cart | {self.id} >< Shopper | {self.shopper.id} >"

    def to_dict(self):
        data = {
            'cart_id': self.id,
            'shopper_id': self.shopper_id,
        }
        items = CartItems.query.filter(CartItems.cart_id == str(self.id)).all()
        if items: 
            data['items'] = items
        else:
            data['items'] = {}
        return data

    def update(self, item, price, quantity):
        self.item = item
        self.price = price
        self.quantity = quantity
        self.total = self.price * self.quantity
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    class CartItems(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False) #references 'cart' in table
        shopper_id = db.Column(db.Integer, db.ForeignKey('shopper.id'), nullable=False) #references 'shopper' in table
        item = db.Column(db.String(50), nullable=False)
        price = db.Column(db.Numeric(8,2), nullable=False)
        quantity = db.Column(db.String(17), nullable=False)
        total = db.Column(db.Numeric(8,2), nullable=False)