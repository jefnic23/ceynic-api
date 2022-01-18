import jwt
import json
import boto3
from time import time
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy, event
from flask_login import UserMixin, current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from passlib.hash import pbkdf2_sha256
from forms import ProductForm
from werkzeug.utils import secure_filename
from paypal_client import PayPalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalhttp.serializers.json_serializer import Json
from paypalhttp.http_error import HttpError
from paypalhttp.encoder import Encoder
from app import app

db = SQLAlchemy()
s3 = boto3.Session(
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
)
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

    def mark_as_sold(self, sold):
        self.sold = True

class ProductModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

    # configure to send path to db, file to pics folder
    def create_form(self):
        form = ProductForm()
        return form

    def on_model_change(self, form, model, is_created):
        file_title = form.title.data.replace(" ", "_")
        file_path = 'public/' + file_title + '/'
        bucket.Object(file_path)
        files = [f for f in form.images.data]
        model.images = []
        for f in files:
            secured_file = secure_filename(f.filename.replace(" ", "_"))
            model.images.append(secured_file)
            bucket.Object(file_path + secured_file).put(Body=f)

@event.listens_for(Product, 'after_delete')
def _handle_image_delete(mapper, conn, target):
    try:
        if target.images:
            for image in target.images:
                path = 'public/' + target.title + '/' + image
                resource.Object(app.config['BUCKET_NAME'], path).delete()
            bucket.Object('public/' + target.title + '/').delete()
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
    def build_request_body():
        return \
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": '123.00'
                        }
                    }
                ]
            }

    def create_order(self):
        request = OrdersCreateRequest()
        request.headers['prefer'] = 'return=representation'
        request.request_body(self.build_request_body())
        response = self.client.execute(request)

        return response

class CaptureOrder(PayPalClient):
    def capture_order(self, order_id):
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)

        return response