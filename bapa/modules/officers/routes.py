from . import controllers
from flask import render_template, redirect, url_for, flash
from flask import session, request
from flask import Blueprint

bp = Blueprint('officers', __name__, template_folder='templates')


@bp.route('/', methods=['GET'])
def index():
    """Display Officer's Dashboard"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    members = controllers.get_members()
    return render_template('dashboard.html', members=members)

@bp.route('/news/post', methods=['POST'])
def post_news():
    """"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    if request.method == 'POST':
        controllers.news_update(
            request.form['subject'],
            request.form['body'],
            session['user']['id']
        )
        return redirect(url_for('home.news'))

@bp.route('/appoint/')
@bp.route('/appoint/<key>', methods=['GET'])
def appoint(key=None):
    """Appoint an officer"""
    if not session.get('user'):
        return redirect(url_for('home.login'))
    message = None
    if key:
        appointer_id = int(session['user'].get('id'))
        user_id = int(request.args.get('user_id') or appointer_id)
        message = controllers.appoint(user_id, appointer_id, key)
        if user_id == appointer_id and 'added' in message:
            session['user']['officer'] = True #TODO: this is actually ineffective in the interface
    else:
        appointer_id = session['user'].get('id')
        user_id = request.args.get('user_id')
        message = controllers.appoint(user_id, appointer_id)
    flash(message)
    return redirect(url_for('home.index'))
