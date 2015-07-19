from . import controllers
from flask import render_template, redirect, url_for, flash
from flask import session, request
from flask import Blueprint

home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/')
def index():
    return render_template('home.html', session=session)


@home_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register the user."""
    if session.get('user_id'):
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



@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if session.get('user_id'):
        return redirect(url_for('home.index'))
    error = None
    if request.method == 'POST':
        user = controllers.authenticate_user(request.form['ushpa'], request.form['password'])
        if user:
            flash('Welcome back, %s' % user['firstname'])
            session['user_id'] = str(user['_id'])
            session['user_ushpa'] = user['ushpa']
            session['firstname'] = user['firstname']
            session.permissions = user['permissions']
            return redirect(url_for('home.index'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error, session=session)



@home_bp.route('/logout')
def logout(msg='You were logged out'):
    """Logs the user out."""
    flash(msg)
    session.clear()
    return redirect(url_for('home.index'))
