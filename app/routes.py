from app import app
from flask import render_template, redirect, url_for, flash

@app.route('/index')
def index():
    return render_template('index.html')