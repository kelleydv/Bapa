from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import date
from . import config

app = Flask(__name__)

app.config.from_object('bapa.config.Develop')

db = SQLAlchemy(app)

mail = Mail(app)

# blueprints
from bapa.modules import blueprints
for prefix, bp in blueprints.items():
    app.register_blueprint(bp, url_prefix=prefix)

# Template Globals
app.jinja_env.globals['year'] = date.today().year
