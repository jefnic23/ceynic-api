import jwt
from time import time
from flask_sqlalchemy import event
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256
from app.forms import *
from app import app, db

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
