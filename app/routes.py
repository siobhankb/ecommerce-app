from app import app
from app.forms import NewShopperForm, LoginForm, AddItemForm
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Shopper, Cart
from flask import render_template, redirect, url_for, flash

@app.route('/')
def index():
    hi = 'hello you'
    return render_template('index.html', hi=hi)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = NewShopperForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # Query user table to make sure info entered is unique
        shopper_check = Shopper.query.filter((Shopper.username == username) | (Shopper.email == email)).all()
        if shopper_check:
            flash('A shopper with that username already exitsts', 'danger')
            return redirect(url_for('signup'))

        # add the user to the database
        new_shopper = Shopper(email=email, username=username, password=password)
        
        # show message of success/failure
        flash(f"'{new_shopper.username}' has successfully signed up!", 'success')
        #redirect to login page
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        shopper = Shopper.query.filter(Shopper.username == username).first()

        if shopper is not None and shopper.check_password(password):
            login_user(shopper)
            flash(f'Welcome back, {shopper.username}', 'primary')
            return redirect(url_for('index'))

        flash('Incorrect username and/or password. Please try again.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('login.html', form=form)

@app.route('/view-cart')
def view_cart():
    if current_user.is_authenticated:
        items=Cart.query.filter(Cart.shopper_id == current_user.id).all()
        return render_template('view_cart.html', items=items)
    else:
        return render_template('view_cart.html', items=[])

@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    return render_template('add_item.html', form=form)

@app.route('/edit-cart', methods=['GET', 'POST'])
def edit_cart():
    return render_template('edit_cart.html')

@app.route('/delete-item')
def delete_item():
    return render_template('delete_item.html')

