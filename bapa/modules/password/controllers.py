from bapa import models
from bapa import app, mail
from bapa.utils import timestamp,is_too_old, get_salt
from bapa.utils import object_from_timestamp, get_hash
from flask_mail import Message


def reset_password_request(ushpa, email, url):
    """Send an email to the user with a token"""
    if not (ushpa and email):
        return 'Please enter your USHPA pilot number and email address'
    elif not (email and '@' in email and '.' in email):
        return 'You have to enter a valid email address'
    else:
        user = models.User.match(email=email)
        if user and user['ushpa'] == ushpa:
            token = get_salt()
            models.ResetPassword().create(
                    user['_id'],
                    timestamp(),
                    token
            )
            body = '%s/%s' % (url,token)
            msg = Message(
                subject='Password Reset - sfbapa.org',
                body=body,
                recipients=[email]
            )
            
            if app.debug:
                print(body)
            else:
                with app.app_context():
                    mail.send(msg)


def reset_password_auth(ushpa, email, token):
    """Authenticate a user using a token"""
    if not (ushpa and email and token):
        return
    else:
        reset = models.ResetPassword.match(token=token)
        if not reset:
            return
        models.ResetPassword.delete(token)
        user = models.User.from_id(reset.get('user_id'))
        if user['email'] == email and user['ushpa'] == ushpa:
            time_requested = object_from_timestamp(reset['timestamp'])
            if not is_too_old(time_requested):
                if reset['token'] == token:
                    return user


def auth(ushpa, password):
    """Authenticate as permission for password reset"""
    return models.User.auth(ushpa, password)

def reset_password(user_id, password, password2):
    """Reset password for an authenticated user"""
    if password != password2:
        return 'Passwords must match'
    models.User.update(user_id, password=get_hash(password))

