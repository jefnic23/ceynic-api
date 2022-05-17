from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, current_user, logout_user
from flask_admin import Admin
from sqlalchemy import func
from app.forms import *
from app.models import *
from app.views import *
from app.paypal import *
from app.email import *
from app import app, login

admin = Admin(app, name="TraceyNicholasArt", index_view=AdminView(), template_mode='bootstrap4')
admin.add_view(ProductModelView(Product, db.session))
admin.add_link(LogoutView(name='Logout', endpoint='logout'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse')
def browse():
    paths = list({f.key.split('/')[1] for f in bucket.objects.all()})
    files = []
    for path in paths:
        painting_obj = Product.query.filter_by(title=path.replace('_', ' ')).first()
        if not painting_obj.sold:
            d = {'id': painting_obj.id, 'path': '', 'filename': ''}
            for obj in bucket.objects.filter(Prefix='public/' + path + '/'):  
                d['path'], d['filename'] = path, obj.key
                files.append(d)
                break
    return render_template('browse.html', bucket=bucket, files=sorted(files, key=lambda x: x['id']))

@app.route('/painting/<path>')
def painting(path):
    product = Product.query.filter_by(title=path.replace('_', ' ')).first()
    if not product.sold:
        low_id = db.session.query(func.min(Product.id)).first()[0]
        hi_id = db.session.query(func.max(Product.id)).first()[0]
        data = {
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "medium": product.medium.value,
            "height": product.height,
            "width": product.width,
            "description": product.description,
            "filenames": [f.key for f in bucket.objects.filter(Prefix='public/' + path + '/')],
            "prev": Product.query.order_by(Product.id.desc()).filter(Product.id < product.id).first().title.replace(' ', '_') if product.id > low_id else Product.query.get(hi_id).title.replace(' ', '_'),
            "next": Product.query.order_by(Product.id.asc()).filter(Product.id > product.id).first().title.replace(' ', '_') if product.id < hi_id else Product.query.get(low_id).title.replace(' ', '_')
        }
        return render_template('painting.html', path=path, data=data)
    else:
        return redirect(url_for('browse'))

@app.route('/create-order', methods=['POST'])
def create_order():
    id = request.get_json()['id']
    product = Product.query.get(id)
    title = product.title
    medium = product.medium
    description = f'{title}, {medium}'
    value = product.price
    order = CreateOrder().create_order(description, value)
    return jsonify({'order_id': order.result.id})

@app.route('/capture-order/<order_id>', methods=['POST'])
def capture_order(order_id):
    order = CaptureOrder().capture_order(order_id)
    status = order.result.status
    purchase_id = order.result.purchase_units[0].payments.captures[0].id
    id = request.get_json()['id']
    product = Product.query.get(id)
    product.sold = True
    product.purchase_id = purchase_id
    db.session.commit()
    return jsonify({'status': status, 'purchase_id': purchase_id})

@app.route('/orderconfirmation/<purchase_id>')
def order_confirmation(purchase_id):
    return render_template('orderconfirmation.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        send_contact_email(contact_form)
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

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == "__main__":
    app.run()
    