from flask import Flask
from config import Config
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import boto3

app=Flask(__name__)
app.config.from_object(Config)
Talisman(app, content_security_policy=None)
db = SQLAlchemy(app)
mail = Mail(app)
s3 = boto3.Session(
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
)

from app import routes, models, errors