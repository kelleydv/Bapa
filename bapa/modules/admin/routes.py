from . import controllers
from flask import render_template, redirect, url_for
from flask import session, request
from flask import Blueprint

bp = Blueprint('admin', __name__, template_folder='templates')


@bp.route('/', methods=['GET'])
def index():
    """Main Administrators page"""
    if not session.get('user') or not session['user'].get('admin'):
        return redirect(url_for('home.login'))
    if request.method == 'GET':
        controllers.foo()
    return render_template('admin.html')
