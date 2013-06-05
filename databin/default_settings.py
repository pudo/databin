
import os

DEBUG = True
ASSETS_DEBUG = True
SECRET_KEY = os.environ.get('SECRET', 'key')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///development.db')
