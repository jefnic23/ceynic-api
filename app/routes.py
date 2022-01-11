from flask import render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from app import app

bootstrap = Bootstrap(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run()