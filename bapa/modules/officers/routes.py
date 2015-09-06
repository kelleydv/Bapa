from . import controllers
from flask import render_template, redirect
from flask import session, request
from flask import Blueprint

offic_bp = Blueprint('officers', __name__, template_folder='templates')


@offic_bp.route('/', methods=['GET'])
def index():
    """Main Officers page"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    if request.method == 'GET':
        members = controllers.get_members()
    return render_template('members.html', members=members)
