from flask import render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from forms import *
from models import *
import os
from app.email import send_password_reset_email
from app import app

bootstrap = Bootstrap(app)
login = LoginManager(app)
login.init_app(app)
admin = Admin(app, index_view=AdminView())
admin.add_view(ProductModelView(Product, db.session))
admin.add_link(LogoutView(name='Logout', endpoint='logout'))

BASE_DIR = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'])

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse')
def browse():
    image_dirs = os.listdir(BASE_DIR)
    images = []
    for dir in image_dirs:
        paths = {'dir': '', 'image': ''}
        filename = os.listdir(os.path.join(BASE_DIR, dir))[0]
        paths['dir'] = dir
        paths['filename'] = filename
        images.append(paths)
    return render_template('browse.html', images=images)

@app.route('/painting/<dir>')
def painting(dir):
    filenames = [f for f in os.listdir(os.path.join(BASE_DIR, dir))]
    return render_template('painting.html', dir=dir, filenames=filenames)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(email=login_form.email.data).first()
        if not user_object or not user_object.check_password(login_form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user_object, remember=login_form.remember_me.data)
        flash('Login successful', 'success')
        return redirect(url_for('admin.index'))
    return render_template("login.html", form=login_form)

@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_anonymous:
        return redirect(url_for("index"))
    logout_user()
    flash("You have logged out successfully", "success")
    return redirect(url_for("login"))

@app.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        db.session.commit()
        if user:
            send_password_reset_email(user)
        flash("Check your email for instructions on how to reset your password", 'info')
        return redirect(url_for('login'))
    return render_template("reset_password_request.html", form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        hashed_pswd = pbkdf2_sha256.hash(password)
        user.set_password(hashed_pswd)
        db.session.commit()
        flash('Your password has been reset', "success")
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

if __name__ == "__main__":
    app.run()