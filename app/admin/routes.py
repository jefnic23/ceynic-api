from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from sqlalchemy import func
from app import db
from app.models import Product
from app.admin import bp


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/product')
@login_required
def product():
    headers = ['title', 'price', 'medium', 'height', 'width', 'description', 'sold', 'slideshow']
    products = Product.query.all()
    return render_template('admin/product.html', headers=headers, products=products)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        medium = request.form['medium']
        height = request.form['height']
        width = request.form['width']
        description = request.form['description']
        slideshow = request.form.get('slideshow')
        flash("Product added.", "success")
        return redirect(url_for('admin.product'))
    else:
        return render_template('admin/create.html')
    

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        print(request.form['title'])
        return '', 204
    else:
        listing = Product.query.get(id)
        files = [f'{current_app.config["AWS_URL"]}{f.key}' for f in current_app.bucket.objects.filter(Prefix=f"public/{listing.title.replace(' ', '_')}/")]
        return render_template('admin/update.html', listing=listing, files=files)


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    print(f"\n{id}\n")
    return render_template('admin/delete.html')
