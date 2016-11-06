from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import date
import os, subprocess

app = Flask(__name__)

#`env` must be set to dev, prod, or test
env = os.environ.get('ENV')
conf = {
    'DEV': 'bapa.config.Develop',
    'PROD': 'bapa.config.Production',
    'TEST': 'bapa.config.Testing'
}[env]
app.config.from_object(conf)

db = SQLAlchemy(app)
db.create_all() #create all tables according to schemae in bapa/models

mail = Mail(app)

# blueprints
from bapa.modules import blueprints
for prefix, bp in blueprints.items():
    app.register_blueprint(bp, url_prefix=prefix)

# Template Globals
app.jinja_env.globals['year'] = date.today().year
head = str(subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip(), "utf-8")
app.jinja_env.globals['commit_hash'] = head[:4]
app.jinja_env.globals['env'] = env.lower()
