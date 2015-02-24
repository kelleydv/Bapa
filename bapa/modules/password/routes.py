from . import controllers
from flask import session, flash
from flask import render_template, redirect, url_for, request
from flask import Blueprint

pass_bp = Blueprint('password', __name__, template_folder='templates')


@pass_bp.route('/reset/request', methods=['GET', 'POST'])
def reset_request():
    if session.get('user_id'):
        return redirect(url_for('home.index'))
    error = None
    if request.method == 'POST':
        error = controllers.reset_password_request(
            request.form['ushpa'],
            request.form['email'],
            url_for('home.login')+'/reset/auth'
        )
        if not error:
            flash('Email sent')
            return redirect(url_for('home.index'))
    return render_template('reset_req.html', error=error)


@pass_bp.route('/reset/auth/<secret>', methods=['GET', 'POST'])
def reset_auth(secret=None):
    if session.get('user_id') or not secret:
        return redirect(url_for('home.index'))
    if request.method == 'POST':
        user = controllers.reset_password_auth(
            request.form['ushpa'],
            request.form['email'],
            secret
        )
        if not user:
            flash('Password Reset Failed')
            return redirect(url_for('home.login'))
        session['user_id'] = str(user['_id'])
        return redirect(url_for('password.reset'))
    flash('Re-enter')
    return render_template('reset_req.html')


@pass_bp.route('/auth', methods=['GET', 'POST'])
def simple_auth():
    if not session.get('user_id'):
        return redirect(url_for('home.index'))
    error = None
    if request.method == 'POST':
        if controllers.auth(session['ushpa'], request.form['password']):
            return redirect(url_for('password.reset'))
        error = 'Enter your current password'
    return render_template('auth.html', error=error)


@pass_bp.route('/reset', methods=['GET', 'POST'])
def reset():
    if not session.get('user_id'):
        return redirect(url_for('home.login'))
    error = None
    if request.method == 'POST':
        error = controllers.reset_password(
            session['user_id'],
            request.form['password'],
            request.form['password2']
        )
        if not error:
            flash('Your password has been reset')
            return redirect(url_for('home.logout'))
    return render_template('reset.html', error=error)

