from . import controllers
from bapa.utils import timestamp, is_too_old
from flask import render_template, redirect, url_for, flash
from flask import session, request
from flask import Blueprint
import markdown2
import os

bp = Blueprint('home', __name__, template_folder='templates')


@bp.route('/')
def index():
    return render_template('home.html', session=session)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register the user."""
    if session.get('user'):
        return redirect(url_for('home.index'))
    error = None
    if request.method == 'POST':
        error = controllers.signup(
            request.form['ushpa'],
            request.form['email'],
            request.form['password'],
            request.form['password2'],
            request.form['firstname'],
            request.form['lastname']
        )
        if not error:
            flash('You were successfully registered and can login now')
            return redirect(url_for('home.login'))
    return render_template('register.html', error=error)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if session.get('user'):
        return redirect(url_for('home.index'))
    error = None
    if request.method == 'POST':
        user = controllers.authenticate_user(request.form['ushpa_or_email'], request.form['password'])
        if user:
            flash('Welcome back, %s' % user['firstname'])
            session['user'] = user
            return redirect(url_for('home.index'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error, session=session)


@bp.route('/logout')
@bp.route('/logout/<msg>')
def logout(msg='You were logged out'):
    """Logs the user out."""
    session.clear()
    flash(msg)
    return redirect(url_for('home.index'))



##################
# Password Reset #
##################

@bp.route('/password/reset/request', methods=['GET', 'POST'])
def reset_request():
    if session.get('user'):
        return redirect(url_for('home.index'))
    error = None
    if request.method == 'POST':
        error = controllers.reset_password_request(
            request.form['email'],
            url_for('home.reset_auth')
        )
        if not error:
            flash('Email sent')
            return redirect(url_for('home.index'))
    return render_template('reset_req.html', error=error)


@bp.route('/password/reset/auth/')
@bp.route('/password/reset/auth/<secret>', methods=['GET', 'POST'])
def reset_auth(secret=None):
    if session.get('user') or not secret:
        return redirect(url_for('home.index'))
    if request.method == 'POST':
        user = controllers.reset_password_auth(
            request.form['email'],
            secret
        )
        if not user:
            flash('Password Reset Failed')
            return redirect(url_for('home.login'))
        session['user'] = {}
        session['user']['id'] = user.id
        session['authed'] = timestamp(object=True)
        return redirect(url_for('home.reset'))
    return render_template('reset_auth.html', secret=secret)


@bp.route('/password/auth', methods=['GET', 'POST'])
def simple_auth():
    if not session.get('user'):
        return redirect(url_for('home.login'))
    error = None
    if request.method == 'POST':
        if controllers.auth(session['user']['email'], request.form['password']):
            session['authed'] = timestamp(object=True)
            return redirect(url_for('home.reset'))
        error = 'Enter your current password'
    return render_template('auth.html', error=error)


@bp.route('/password/reset', methods=['GET', 'POST'])
def reset():
    if not session.get('user'):
        return redirect(url_for('home.login'))
    if is_too_old(session.get('authed')):
        return redirect(url_for('home.simple_auth'))
    error = None
    if request.method == 'POST':
        error = controllers.reset_password(
            session['user']['id'],
            request.form['password'],
            request.form['password2']
        )
        if not error:
            return redirect(url_for('home.logout', msg='Your password has been reset'))
    return render_template('reset.html', error=error)


@bp.route('/page/<name>')
def page(name=None):
    path = os.path.join(os.getcwd(), 'bapa', 'content', name + '.md')

    if not os.path.isfile(path):
        # TODO Create a 404 page
        flash('Page not found')
        return redirect(url_for('home.index'))

    with open(path) as f:
        text = f.read()
        content = markdown2.markdown(text)
        title = text.split('\n').pop(0)[2:].strip()

    return render_template('pages/page.html', title=title, content=content)


@bp.route('/news', methods=['GET'])
def news():
    page = request.args.get('page')
    n = 3 #per page
    if page:
        page = int(page)
    if not page or page < 1:
        page = 1

    #officers may need to edit posts
    editable = False
    if request.args.get('edit'):
        if session.get('user') and session['user'].get('officer'):
            editable = True
    entries = controllers.get_news_entries(page, n)
    return render_template('news.html', entries=entries, page=page, n=n, editable=editable)
