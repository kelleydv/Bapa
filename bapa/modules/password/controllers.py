from bapa.models import User, ResetPassword
from bapa import app, mail, db
from bapa.utils import timestamp, is_too_old, get_salt
from bapa.utils import object_from_timestamp, get_hash
from flask_mail import Message

import os, string


def reset_password_request(ushpa, email, url):
    """Send an email to the user with a token"""
    if not (ushpa and email):
        return 'Please enter your USHPA pilot number and email address'
    elif not (email and '@' in email and '.' in email):
        return 'You have to enter a valid email address'
    else:
        user = User.query.filter_by(email=email).first()
        if user and str(user.ushpa) == ushpa:
            token = get_salt()[:32]
            reset = ResetPassword(
                user.id,
                token
            )
            db.session.add(reset)
            db.session.commit()

            url = app.config['HOST'] + url
            url = url + token
            email_path = os.path.join(os.getcwd(), 'bapa', 'emails', 'reset.txt')
            name = user.firstname
            with open(email_path, 'r') as f:
                t = f.read()
                body = string.Template(t).substitute(url=url, name=name, host=app.config['HOST'])

            msg = Message(
                subject='Password Reset - sfbapa.org',
                body=body,
                recipients=[email]
            )
            if app.debug and not os.environ.get('HEROKU'):
                print(body)
            else:
                with app.app_context():
                    mail.send(msg)


def reset_password_auth(ushpa, email, token):
    """Authenticate a user using a token"""
    if not (ushpa and email and token):
        return
    else:
        reset = ResetPassword.query.filter_by(token=token).first()
        if not reset:
            return
        ResetPassword.query.filter_by(token=token).delete()
        user = User.query.get(reset.user_id)
        if user.email == email and str(user.ushpa) == ushpa:
            time_requested = reset.created_at
            if not is_too_old(time_requested):
                if reset.token == token:
                    return user


def auth(ushpa, password):
    """Authenticate as permission for password reset"""
    user = User.query.filter_by(ushpa=ushpa).first()
    if not user and verify_hash(password, user.password):
        return
    return True

def reset_password(user_id, password, password2):
    """Reset password for an authenticated user"""
    if password != password2:
        return 'Passwords must match'
    User.user_id = get_hash(password)
    db.session.commit
