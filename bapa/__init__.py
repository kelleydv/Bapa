from flask import Flask, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import date, datetime
import os, subprocess

app = Flask(__name__)

env = os.environ.get('ENV', 'DEV')
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
from bapa.modules.officers.controllers import is_officer
from bapa.modules.membership.controllers import is_member
from bapa.utils import parse_ratings
app.jinja_env.globals.update(is_officer=lambda user_id: False if session.get('user', {}).get('officer') is False else is_officer(user_id))
app.jinja_env.globals.update(is_member=is_member)
app.jinja_env.globals.update(is_this_year=lambda x: False if not x else x >= datetime(year=datetime.now().year, month=1, day=1))
app.jinja_env.globals.update(parse_ratings=parse_ratings)
app.jinja_env.globals.update(date_parse=lambda s:str(s).split(' ')[0])
app.jinja_env.globals['year'] = date.today().year
app.jinja_env.globals['env'] = env.lower()
head = os.environ.get('HEROKU_SLUG_COMMIT') or str(subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip(), "utf-8")
app.jinja_env.globals['commit_hash'] = head[:4]
# For HEROKU_SLUG_COMMIT variable:
# $ heroku labs:enable runtime-dyno-metadata -a <app name>
# https://devcenter.heroku.com/articles/dyno-metadata)
# with GitHub integrations on Heroku, there is no .git repo
# on the server. This is the fix.
