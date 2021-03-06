from . import controllers
from bapa.modules.officers import controllers as officers
from bapa import app
from bapa.utils import timestamp, is_too_old
from bapa.decorators.auth import redirect_authenticated, require_auth
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
@redirect_authenticated
def register():
    """Register the user."""

    error = None
    if request.method == 'POST':

        error = controllers.signup(
            request.form['ushpa'],
            request.form['email'],
            request.form['password'],
            request.form['password2'],
            request.form['firstname'],
            request.form['lastname'],
            request.form.get('g-recaptcha-response')
        )
        if not error:
            flash('You were successfully registered and can login now')
            return redirect(url_for('home.login'))
    return render_template('register.html', error=error, recaptcha=app.config.get('RECAPTCHA'), sitekey=app.config.get('RECAPTCHA_SITEKEY'))


@bp.route('/login', methods=['GET', 'POST'])
@redirect_authenticated
def login():
    """User login"""

    error = None
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        user = controllers.authenticate_user(request.form['ushpa_or_email'], request.form['password'], recaptcha_response)
        if user:
            flash('Welcome back, %s' % user['firstname'])
            session['user'] = user
            return redirect(url_for('home.index'))
        else:
            error = 'Invalid credentials or reCaptcha'
    return render_template('login.html', error=error, session=session, recaptcha=app.config.get('RECAPTCHA'), sitekey=app.config.get('RECAPTCHA_SITEKEY'))


@bp.route('/logout')
@bp.route('/logout/<msg>')
def logout(msg='You were logged out'):
    """Logs the user out."""
    session.clear()
    flash(msg)
    return redirect(url_for('home.index'))

@bp.route('/account/delete')
@require_auth
def delete_account():
    """Delete user account. Cannot be undone."""
    controllers.delete_account(session['user']['id'])
    flash('Your account has been deleted')
    return redirect(url_for('home.logout'))





##################
# Password Reset #
##################

@bp.route('/password/reset/request', methods=['GET', 'POST'])
@redirect_authenticated
def reset_request():
    """Request a password reset token to be sent via email"""

    error = None
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        error = controllers.reset_password_request(
            request.form['ushpa_or_email'],
            url_for('home.reset_auth'),
            recaptcha_response
        )
        if not error:
            flash('Email sent')
            return redirect(url_for('home.index'))
    return render_template('reset_req.html', error=error, recaptcha=app.config.get('RECAPTCHA'), sitekey=app.config.get('RECAPTCHA_SITEKEY'))


@bp.route('/password/reset/auth/')
@bp.route('/password/reset/auth/<secret>', methods=['GET', 'POST'])
@redirect_authenticated
def reset_auth(secret=None):
    if not secret:
        return redirect(url_for('home.index'))
    if request.method == 'POST':
        user = controllers.reset_password_auth(
            request.form['ushpa_or_email'],
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
@require_auth
def simple_auth():
    """Authed user re-enters password for critical actions"""

    error = None
    if request.method == 'POST':
        if controllers.auth(session['user']['email'], request.form['password']):
            session['authed'] = timestamp(object=True)
            return redirect(url_for('home.reset'))
        error = 'Enter your current password'
    return render_template('auth.html', error=error)


@bp.route('/password/reset', methods=['GET', 'POST'])
@require_auth
def reset():
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

@bp.route('/club', methods=['GET'])
def club():
    return render_template('pages/club.html',
        officers=officers.get_officers(),
        google_api_key=app.config.get('GOOGLE_API_KEY'),
        google_cal_id=app.config.get('GOOGLE_CAL_ID'),
        session=session)
