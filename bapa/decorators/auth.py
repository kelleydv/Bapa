"""Auth Decorators"""

from functools import wraps
from flask import request, redirect, session, url_for

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('home.login'))
        return f(*args, **kwargs)
    return decorated_function


def redirect_authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user'):
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)
    return decorated_function

def require_officer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user') or not session['user'].get('officer'):
            return redirect(url_for('home.login'))
        return f(*args, **kwargs)
    return decorated_function
