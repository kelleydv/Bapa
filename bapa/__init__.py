from flask import Flask, url_for
from flask_mail import Mail
from datetime import date

app = Flask(__name__)

app.config.from_envvar('BAPA_CONF')

# Template Globals
app.jinja_env.globals['year'] = date.today().year

mail = Mail(app)

from bapa.modules import home, account, password # blueprints

app.register_blueprint(home.home_bp)
app.register_blueprint(account.acct_bp, url_prefix='/account')
app.register_blueprint(password.pass_bp, url_prefix='/password')
