from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class Shopper(FlaskForm):
    username = StringField('Username', validators=[DataRequired])
