import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    AWS_ACCESS_KEY_ID = os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID')
    AWS_REGION = os.environ.get('BUCKETEER_AWS_REGION')
    AWS_SECRET_ACCESS_KEY = os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY')
    BUCKET_NAME = os.environ.get('BUCKETEER_BUCKET_NAME')
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')
    FLASK_ADMIN_SWATCH = os.environ.get('FLASK_ADMIN_SWATCH')
    DROPZONE_ALLOWED_FILE_TYPE = os.environ.get('DROPZONE_ALLOWED_FILE_TYPE')