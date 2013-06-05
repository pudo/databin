import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from databin import default_settings

logging.basicConfig(level=logging.WARN)

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('DATABIN_SETTINGS', silent=True)

db = SQLAlchemy(app)
