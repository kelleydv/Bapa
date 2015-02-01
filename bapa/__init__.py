import os
from flask import Flask

from bapa import home, account # blueprints

app = Flask(__name__)
app.secret_key = os.environ['bapa_session_secret']

app.register_blueprint(home.bp)
app.register_blueprint(account.bp, url_prefix='/account')

