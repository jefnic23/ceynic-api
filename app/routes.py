from flask import render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from forms import ContactForm
import glob, os
from app import app

bootstrap = Bootstrap(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/browse')
def browse():
    pics = [os.path.basename(f) for f in glob.glob('app/static/pics/*.jpg')]
    return render_template('browse.html', pics=pics)

@app.route('/painting/<filename>')
def painting(filename):
    return render_template('painting.html', filename=filename)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        flash('Thank you for the message!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=contact_form)

if __name__ == "__main__":
    app.run()