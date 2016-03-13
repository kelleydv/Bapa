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
from bapa.modules import home, membership, password, officers, admin
app.register_blueprint(home.home_bp)
app.register_blueprint(membership.memb_bp, url_prefix='/membership')
app.register_blueprint(password.pass_bp, url_prefix='/password')
app.register_blueprint(officers.offic_bp, url_prefix='/officers')
app.register_blueprint(admin.admin_bp, url_prefix='/admin')

# Template Globals
app.jinja_env.globals['year'] = date.today().year
