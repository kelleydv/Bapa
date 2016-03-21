from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import date
import os

app = Flask(__name__)

env = os.environ.get('env')
conf = {
    'dev': 'bapa.config.Develop',
    'prod': 'bapa.config.Production',
    'test': 'bapa.config.Testing'
}[env]
app.config.from_object(conf)

db = SQLAlchemy(app)

mail = Mail(app)

# blueprints
from bapa.modules import blueprints
for prefix, bp in blueprints.items():
    app.register_blueprint(bp, url_prefix=prefix)

# Template Globals
app.jinja_env.globals['year'] = date.today().year
