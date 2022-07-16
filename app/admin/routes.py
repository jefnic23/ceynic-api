from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
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
    page = request.args.get('page', 1, type=int)
    headers = ['title', 'price', 'medium', 'height', 'width', 'description', 'sold', 'slideshow']
    products = Product.query.order_by(Product.id.asc()).paginate(page, 15, False)
    next_url = url_for('admin.product', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('admin.product', page=products.prev_num) \
        if products.has_prev else None
    return render_template(
        'admin/product.html', 
        headers=headers, 
        products=products.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # create new listing in database
        title = request.form['title']
        price = request.form['price']
        medium = request.form['medium']
        height = request.form['height']
        width = request.form['width']
        description = request.form['description']
        slideshow = request.form.get('slideshow')
        new_listing = Product(
            title=title,
            price=price,
            medium=medium,
            height=height,
            width=width,
            description=description,
            slideshow=slideshow,
        )
        db.session.add(new_listing)
        db.session.commit()

        # add images to S3 bucket
        images = request.files.getlist('images')
        path = f"public/{title.replace(' ', '_')}/"
        for image in images:
            secured_file = secure_filename(image.filename.replace(" ", "_"))
            current_app.bucket.Object(path + secured_file).put(Body=image)

        flash("Product added", "success")
        return redirect(url_for('admin.product'))
    else:
        return render_template('admin/create.html')
    

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    listing = Product.query.get(id)
    if request.method == 'POST':
        # update database with new info
        listing.title = request.form['title']
        listing.price = request.form['price']
        listing.medium = request.form['medium']
        listing.height = request.form['height']
        listing.width = request.form['width']
        listing.description = request.form['description']
        listing.slideshow = request.form.get('slideshow')
        listing.sold = request.form.get('sold')
        db.session.commit()

        # remove images from S3 bucket
        prefix = f"public/{listing.title.replace(' ', '_')}/"
        current_app.bucket.objects.filter(Prefix=prefix).delete()

        # upload new images to S3 bucket
        images = request.files.getlist('images')
        path = f"public/{listing.title.replace(' ', '_')}/"
        for image in images:
            secured_file = secure_filename(image.filename.replace(" ", "_"))
            current_app.bucket.Object(path + secured_file).put(Body=image)

        flash("Product updated", "success")
        return redirect(url_for('admin.product'))
    else:
        files = [f'{current_app.config["AWS_URL"]}{f.key}' for f in current_app.bucket.objects.filter(Prefix=f"public/{listing.title.replace(' ', '_')}/")]
        return render_template('admin/update.html', listing=listing, files=files)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    listing = Product.query.get(id)
    if request.method == "POST":
        # delete listing from database
        db.session.delete(listing)
        db.session.commit()

        # remove images from S3 bucket
        prefix = f"public/{listing.title.replace(' ', '_')}/"
        current_app.bucket.objects.filter(Prefix=prefix).delete()

        flash("Product deleted", "success")
        return redirect(url_for('admin.product'))
    else:
        return render_template('admin/delete.html', listing=listing)
