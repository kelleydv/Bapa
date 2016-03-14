from . import controllers
from flask import render_template, redirect, url_for, flash
from flask import session, request
from flask import Blueprint

bp = Blueprint('officers', __name__, template_folder='templates')


@bp.route('/', methods=['GET'])
def index():
    """"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    return redirect(url_for('officers.post_news'))

@bp.route('/news/post', methods=['GET', 'POST'])
def post_news():
    """"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    if request.method == 'GET':
        return render_template('new_post.html', page='news')
    if request.method == 'POST':
        controllers.news_update(
            request.form['subject'],
            request.form['body'],
            session['user']['id']
        )
        return redirect(url_for('home.news'))


@bp.route('/members', methods=['GET'])
def view_members():
    """Main Officers page"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    if request.method == 'GET':
        members = controllers.get_members()
    return render_template('members.html', members=members, page='members')


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
        message = controllers.appoint(appointer_id, user_id, key)
        if user_id == appointer_id and 'added' in message:
            session['user']['officer'] = True #TODO: this is actually ineffective in the interface
    else:
        appointer_id = session['user'].get('id')
        user_id = request.args.get('user_id')
        message = controllers.appoint(user_id, appointer_id)
    flash(message)
    return redirect(url_for('home.index'))
