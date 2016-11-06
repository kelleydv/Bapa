from . import controllers
from bapa.decorators.auth import require_auth, require_officer
from flask import render_template, redirect, url_for, flash, g
from flask import session, request
from flask import Blueprint

bp = Blueprint('officers', __name__, template_folder='templates')


@bp.route('/', methods=['GET'])
@require_officer
def index():
    """Display Officer's Dashboard"""
    members = controllers.get_members()
    return render_template('dashboard.html', members=members)

@bp.route('/news/post', methods=['POST'])
@require_officer
def post_news():
    """Post to news feed"""
    if request.method == 'POST':
        controllers.news_update(
            request.form['subject'],
            request.form['body'],
            session['user']['id'],
            request.form.get('news_id')
        )
        return redirect(url_for('home.news'))

@bp.route('/news/delete', methods=['POST'])
@require_officer
def delete_news():
    """Delete a news post"""
    if request.method == 'POST':
        controllers.delete_news(request.form['post_id'])
        return redirect(url_for('home.news'))

@bp.route('/news/edit', methods=['GET'])
@require_officer
def edit_news():
    """Edit a news post"""
    news_id = request.args.get('news_id')
    news_subject, news_body = controllers.get_news(news_id)
    members = controllers.get_members()
    return render_template('dashboard.html',
        members=members, news_subject=news_subject, news_body=news_body, news_id=news_id)

@bp.route('/appoint/')
@bp.route('/appoint/<key>', methods=['GET'])
@require_auth
def appoint(key=None):
    """Appoint an officer"""
    message = None
    if key:
        appointer_id = int(session['user'].get('id'))
        user_id = int(request.args.get('user_id') or appointer_id)
        message = controllers.appoint(user_id, appointer_id, key)
        if user_id == appointer_id and 'added' in message:
            session['user']['officer'] = True
    else:
        appointer_id = session['user'].get('id')
        user_id = request.args.get('user_id')
        message = controllers.appoint(user_id, appointer_id)
    flash(message)
    return redirect(url_for('membership.profile', user_id=user_id))

@bp.route('/normal', methods=['GET'])
@require_officer
def view_as_normal():
    """Remove officer permissions for current session."""
    del session['user']['officer']
    flash('You are no longer viewing as an officer. Logout to reset your permissions.')
    return redirect(url_for('home.index'))
