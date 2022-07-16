# from email.policy import default
import jwt
from enum import Enum
from time import time
from flask import current_app
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256
from app import db, login


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
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# delete once column gets changed to string
class Medium(Enum):
    PAINTING = "painting"
    PRINT = "print"


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    medium = db.Column(db.Enum(Medium), default=Medium.PAINTING, nullable=False) # change to string, add options in form
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), nullable=False)
    sold = db.Column(db.Boolean, default=False)
    slideshow = db.Column(db.Boolean, default=False)
    images = db.Column(db.ARRAY(db.String())) # no need for this
    purchase_id = db.Column(db.String())

    def mark_as_sold(self):
        self.sold = True
