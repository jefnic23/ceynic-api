from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from passlib.hash import pbkdf2_sha256
from app import db
from app.auth import bp
from app.auth.forms import *
from app.models import User
from app.auth.email import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(email=login_form.email.data).first()
        if not user_object or not user_object.check_password(login_form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user_object, remember=login_form.remember_me.data)
        flash('Login successful', 'success')
        return redirect(url_for('admin.index'))
    return render_template("auth/login.html", form=login_form)


@bp.route('/logout', methods=['GET'])
def logout():
    if current_user.is_anonymous:
        return redirect(url_for("main.index"))
    logout_user()
    flash("You have logged out successfully", "success")
    return redirect(url_for("auth.login"))


@bp.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for instructions on how to reset your password", 'info')
        return redirect(url_for('auth.login'))
    return render_template("auth/reset_password_request.html", form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        hashed_pswd = pbkdf2_sha256.hash(password)
        user.set_password(hashed_pswd)
        db.session.commit()
        flash('Your password has been reset', "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
    