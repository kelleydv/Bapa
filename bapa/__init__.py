from flask import Flask, url_for
from flask_mail import Mail
from flask import json

app = Flask(__name__)

app.config.from_envvar('BAPA_CONF')

mail = Mail(app)

from bapa.modules import home, account, password # blueprints

app.register_blueprint(home.home_bp)
app.register_blueprint(account.acct_bp, url_prefix='/account')
app.register_blueprint(password.pass_bp, url_prefix='/password')
