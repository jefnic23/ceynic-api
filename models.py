import os
import jwt
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
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
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
    medium = db.Column(db.String(), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), nullable=False)
    images = db.Column(db.ARRAY(db.String()))

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
        file_path = 'public/' + form.title.data + '/'
        bucket.Object(file_path)
        files = [f for f in form.images.data]
        model.images = []
        for f in files:
            secured_file = secure_filename(f.filename)
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

class PayPalClient:
    def __init__(self):
        self.client_id =  os.environ["PAYPAL-CLIENT-ID"] if 'PAYPAL-CLIENT-ID' in os.environ else "PAYPAL-CLIENT-ID"
        self.client_secret = os.environ["PAYPAL-CLIENT-SECRET"] if 'PAYPAL_CLIENT_SECRET' in os.environ else "PAYPAL-CLIENT-SECRET"
        """Set up and return PayPal Python SDK environment with PayPal Access credentials.
           This sample uses SandboxEnvironment. In production, use
           LiveEnvironment."""
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        """ Returns PayPal HTTP client instance in an environment with access credentials. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)
    