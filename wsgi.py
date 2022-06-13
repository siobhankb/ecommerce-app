from app import app, db
from app.models import Shopper, Cart

@app.shell_context_processor
def make_context():
    return {'db':db, 'Cart': Cart, 'Shopper': Shopper}

@app.before_first_request
def create_tables():
    db.create_all()