from . import controllers
from flask import render_template, redirect, url_for, flash, g
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
            session['user']['id'],
            request.form.get('news_id')
        )
        return redirect(url_for('home.news'))

@bp.route('/news/delete', methods=['POST'])
def delete_news():
    """"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    if request.method == 'POST':
        controllers.delete_news(request.form['post_id'])
        return redirect(url_for('home.news'))

@bp.route('/news/edit', methods=['GET'])
def edit_news():
    """"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    news_id = request.args.get('news_id')
    news_subject, news_body = controllers.get_news(news_id)
    members = controllers.get_members()
    return render_template('dashboard.html',
        members=members, news_subject=news_subject, news_body=news_body, news_id=news_id)

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
    return redirect(url_for('membership.profile', user_id=user_id))

@bp.route('/normal', methods=['GET'])
def view_as_normal():
    """Remove officer permissions for current session."""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    del session['user']['officer']
    flash('You are no longer viewing as an officer. Logout to reset your permissions.')
    return redirect(url_for('home.index'))
