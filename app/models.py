import jwt
from time import time
from flask import redirect, url_for
from flask_sqlalchemy import event
from flask_login import UserMixin, current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from passlib.hash import pbkdf2_sha256
from app.forms import *
from werkzeug.utils import secure_filename
from app.paypal_client import PayPalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from app import app, db, s3

resource = s3.resource('s3', region_name=app.config['AWS_REGION'])
bucket = resource.Bucket(app.config['BUCKET_NAME'])

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def set_password(self, password):
        self.password = password

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    medium = db.Column(db.String(), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), nullable=False)
    sold = db.Column(db.Boolean, default=False)
    images = db.Column(db.ARRAY(db.String()))
    purchase_id = db.Column(db.String())

    def mark_as_sold(self):
        self.sold = True

class ProductModelView(ModelView):

    column_exclude_list = ('purchase_id') # does this need to be visible?
    form_excluded_columns = ('purchase_id')

    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

    def create_form(self):
        form = ProductForm()
        return form

    # add extra column that displays current images?
    def get_edit_form(self):
        form = super(ProductModelView, self).get_edit_form() 
        form.images = MultipleFileField('Upload image(s)')
        return form

    def edit_form(self, obj=None):
        form = super(ProductModelView, self).edit_form(obj) 
        form.images.data = obj.images
        return form

    def on_model_change(self, form, model, is_created=False):
        # check if images added, skip duplicates
        file_title = form.title.data.replace(" ", "_")
        file_path = 'public/' + file_title + '/'
        bucket.Object(file_path)
        files = [f for f in form.images.data]
        if files:
            model.images = []
            for f in files:
                if f:
                    try:
                        secured_file = secure_filename(f.filename.replace(" ", "_"))
                        model.images.append(secured_file)
                        bucket.Object(file_path + secured_file).put(Body=f)
                    except AttributeError:
                        model.images.append(f)

@event.listens_for(Product, 'after_delete')
def _handle_image_delete(mapper, conn, target):
    try:
        if target.images:
            for image in target.images:
                path = 'public/' + target.title.replace(" ", "_") + '/' + image
                resource.Object(app.config['BUCKET_NAME'], path).delete()
            bucket.Object('public/' + target.title.replace(" ", "_") + '/').delete()
    except:
        pass

class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

class LogoutView(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated
    
class CreateOrder(PayPalClient):
    @staticmethod
    def build_request_body(description, value):
        return \
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "description": description,
                        "amount": {
                            "currency_code": "USD",
                            "value": value
                        }
                    }
                ]
            }

    def create_order(self, description, value):
        request = OrdersCreateRequest()
        request.headers['prefer'] = 'return=representation'
        request.request_body(self.build_request_body(description, value))
        response = self.client.execute(request)
        # print(response.result.__dict__)
        return response

class CaptureOrder(PayPalClient):
    def capture_order(self, order_id):
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)
        # print(response.result.__dict__)
        return response
