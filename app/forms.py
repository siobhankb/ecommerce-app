from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email

class NewShopperForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = DecimalField('Price', places=2, rounding='ROUND_UP', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to Cart')