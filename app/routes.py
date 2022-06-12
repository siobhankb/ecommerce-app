from app import app
from flask import render_template, redirect, url_for, flash

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/edit-cart')
def edit_cart():
    return render_template('edit_cart.html')

