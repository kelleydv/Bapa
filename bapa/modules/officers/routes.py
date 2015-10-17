from . import controllers
from flask import render_template, redirect, url_for
from flask import session, request
from flask import Blueprint

offic_bp = Blueprint('officers', __name__, template_folder='templates')


@offic_bp.route('/', methods=['GET'])
def index():
    """"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    return redirect(url_for('officers.post_news'))

@offic_bp.route('/news/post', methods=['GET', 'POST'])
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
            session['user']['_id']
        )
        return redirect(url_for('home.news'))

@offic_bp.route('/news/preview', methods=['GET', 'POST'])
def preview_post():
    """TODO: markdown preview"""
    return redirect(url_for('.post_news'))

@offic_bp.route('/members', methods=['GET'])
def view_members():
    """Main Officers page"""
    if not session.get('user') or not session['user'].get('officer'):
        return redirect(url_for('home.login'))
    if request.method == 'GET':
        members = controllers.get_members()
    return render_template('members.html', members=members, page='members')
