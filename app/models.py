from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class ClassName(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)