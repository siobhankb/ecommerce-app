from app import app
from flask import render_template#, redirect, url_for, flash

@app.route('/index')
def index():
    hi = 'hello you'
    return render_template('index.html', hi=hi)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/view-cart')
def view_cart():
    return render_template('view_cart.html')

@app.route('/add-item')
def add_item():
    return render_template('add_item.html')

@app.route('/edit-cart')
def edit_cart():
    return render_template('edit_cart.html')

@app.route('/delete-item')
def delete_item():
    return render_template('delete_item.html')

