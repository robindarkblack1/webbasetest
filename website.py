from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('web/index.html')

@app.route('/about')
def about():
    return render_template('web/toolsweb/about.html')

@app.route('/signup')
def signup():
    return render_template('web/toolsweb/signup.html')

@app.route('/tools')
def tools():
    return render_template('web/toolsweb/tools.html')

@app.route('/contact')
def contact():
    return render_template('web/toolsweb/contact.html')

@app.route('/login')
def login():
    return render_template('web/toolsweb/login.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)