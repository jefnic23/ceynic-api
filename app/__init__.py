from flask import Flask
from config import Config
from flask_talisman import Talisman
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import boto3

app=Flask(__name__)
app.config.from_object(Config)
Talisman(app, content_security_policy=None)
# csrf = SeaSurf(app)
db = SQLAlchemy(app)
mail = Mail(app)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.init_app(app)

s3 = boto3.Session(
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
)
resource = s3.resource('s3', region_name=app.config['AWS_REGION'])
bucket = resource.Bucket(app.config['BUCKET_NAME'])

from app import routes, models, errors, views