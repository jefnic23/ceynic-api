from flask import render_template, redirect, url_for, flash, jsonify, request, current_app
from sqlalchemy import func
from app import db
from app.models import Product
from app.paypal import CreateOrder, CaptureOrder
from app.main.forms import ContactForm
from app.main.email import send_contact_email
from app.main import bp


@bp.route('/')
def index():
    images = Product.query.filter_by(slideshow=True).all()
    slideshow = {
        "titles": [],
        "images": []
    }
    for image in images:
        slideshow['titles'].append(image.title.replace(' ', '_'))
        slideshow['images'].append([f'{current_app.config["AWS_URL"]}{f.key}' for f in current_app.bucket.objects.filter(Prefix='public/' + image.title.replace(' ', '_') + '/')][0])
    return render_template('index.html', slideshow=slideshow)


@bp.route('/browse')
def browse():
    paths = list({f.key.split('/')[1] for f in current_app.bucket.objects.all()})
    files = []
    for path in paths:
        try:
            painting_obj = Product.query.filter_by(title=path.replace('_', ' ')).first()
            if not painting_obj.sold:
                d = {'id': painting_obj.id, 'path': '', 'filename': ''}
                for obj in current_app.bucket.objects.filter(Prefix='public/' + path + '/'):  
                    d['path'], d['filename'] = path, current_app.config['AWS_URL'] + obj.key
                    files.append(d)
                    break
        except:
            pass
    return render_template('browse.html', bucket=current_app.bucket, files=sorted(files, key=lambda x: x['id']))


@bp.route('/painting/<path>')
def painting(path):
    product = Product.query.filter_by(title=path.replace('_', ' ')).first()
    if not product.sold:
        low_id = db.session.query(func.min(Product.id)).first()[0]
        hi_id = db.session.query(func.max(Product.id)).first()[0]
        data = {
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "medium": product.medium,
            "height": product.height,
            "width": product.width,
            "description": product.description,
            "filenames": [f'{current_app.config["AWS_URL"]}{f.key}' for f in current_app.bucket.objects.filter(Prefix='public/' + path + '/')],
            "prev": Product.query.order_by(Product.id.desc()).filter(Product.id < product.id).first().title.replace(' ', '_') if product.id > low_id else Product.query.get(hi_id).title.replace(' ', '_'),
            "next": Product.query.order_by(Product.id.asc()).filter(Product.id > product.id).first().title.replace(' ', '_') if product.id < hi_id else Product.query.get(low_id).title.replace(' ', '_')
        }
        return render_template('painting.html', path=path, data=data)
    else:
        return redirect(url_for('main.browse'))


@bp.route('/create-order', methods=['POST'])
def create_order():
    id = request.get_json()['id']
    product = Product.query.get(id)
    title = product.title
    medium = product.medium
    description = f'{title}, {medium}'
    value = product.price
    order = CreateOrder().create_order(description, value)
    return jsonify({'order_id': order.result.id})


@bp.route('/capture-order/<order_id>', methods=['POST'])
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


@bp.route('/orderconfirmation/<purchase_id>')
def order_confirmation(purchase_id):
    return render_template('orderconfirmation.html')


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        send_contact_email(contact_form)
        flash('Thank you for the message!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=contact_form)
