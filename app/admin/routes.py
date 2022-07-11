from flask import render_template, redirect, url_for, flash, jsonify, request, current_app
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
        print(f'\n{request.files}\n')
        flash("Product added.", "success")
        return '', 204
    else:
        return render_template('admin/create.html')
    

@bp.route('/update/<int:id>')
@login_required
def update(id):
    return render_template('admin/update.html')


@bp.route('/delete')
@login_required
def delete():
    return render_template('admin/delete.html')
