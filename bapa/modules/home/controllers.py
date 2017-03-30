from bapa import app, db, services
from bapa.services import get_pilot_data, verify_recaptcha, send_email
from bapa.models import User, ResetPassword, Officer, Admin, News, Payment, Profile
from bapa.utils import is_too_old
from bapa.utils import get_salt, get_hash, verify_hash, timestamp
import markdown2
import string
import os
from urllib.parse import urljoin


def authenticate_user(ushpa_or_email, password, recaptcha_response):
    """
    Authenticate and return user record from
    database, None on failed auth.  Prepare for
    use as session data.
    """
    if app.config.get('RECAPTCHA') and not verify_recaptcha(recaptcha_response):
        return

    if '@' in ushpa_or_email:
        user = User.query.filter_by(email=ushpa_or_email).first()
    else:
        user = User.query.filter_by(ushpa=ushpa_or_email).first()

    if not (user and verify_hash(password, user.password)):
        return

    user.last_login = timestamp(object=True)
    user = user.__dict__
    del user['_sa_instance_state'] #non-serializable

    # Add officer and admin data
    if Officer.query.filter_by(user_id=user['id']).first():
        user['officer'] = True
    if Admin.query.filter_by(user_id=user['id']).first():
        user['admin'] = True

    # Add membership status
    dues = Payment.query.filter_by(user_id=user['id'], item='Membership Dues').order_by(Payment.created_at.desc()).first()
    if dues:
        if not is_too_old(dues.created_at, years=1):
            user['member'] = True
    return user


def signup(ushpa, email, password, password2, firstname, lastname, recaptcha_response):
    """Register the user, return error or None."""
    if not (email and '@' in email and '.' in email):
        error = 'You have to enter a valid email address'
    elif ushpa and User.query.filter_by(ushpa=ushpa).first():
        error = 'This USHPA pilot number is already in use by a current BAPA member'
    elif User.query.filter_by(email=email).first():
        error = 'This email is already in use by a current BAPA member'
    elif not password:
        error = 'You have to enter a password'
    elif password != password2:
        error = 'The two passwords do not match'
    elif app.config.get('RECAPTCHA') and not verify_recaptcha(recaptcha_response):
        error = 'reCAPTCHA test failed'
    else:
        # Insert user into database.
        ushpa_data = get_pilot_data(ushpa)
        user = User(
            ushpa,
            ushpa_data,
            email.lower(),
            get_hash(password),
            firstname.capitalize(),
            lastname.capitalize()
        )
        db.session.add(user)
        db.session.commit()
        db.session.add(Profile(user.id))
        db.session.commit()
        return
    return error

def delete_account(user_id):
    """Delete a user account"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return


def reset_password_request(ushpa_or_email, url, recaptcha_response):
    """
    Send an email to the user with a token

    The specified url represents the endpoint the user recieves in
    an email for resetting their password.
    """
    if not ushpa_or_email:
        return 'Please enter an email or pilot number associated with your account'
    elif not ('@' in ushpa_or_email and '.' in ushpa_or_email) and len(ushpa_or_email) != 5:
        return 'That was not a valid entry'
    if app.config.get('RECAPTCHA') and not verify_recaptcha(recaptcha_response):
        return 'reCAPTCHA test failed'
    else:
        if '@' in ushpa_or_email:
            user = User.query.filter_by(email=ushpa_or_email.lower()).first()
        else:
            user = User.query.filter_by(ushpa=ushpa_or_email).first()
        if user:
            token = get_salt()[:32]
            reset = ResetPassword(
                user.id,
                token
            )
            db.session.add(reset)
            db.session.commit()

            url = urljoin(app.config['HOST'], url)
            url = urljoin(url, token)
            email_path = os.path.join(os.getcwd(), 'bapa', 'emails', 'reset.txt')
            name = user.firstname
            with open(email_path, 'r') as f:
                t = f.read()
                body = string.Template(t).substitute(url=url, name=name, host=app.config['HOST'])

            send_email(
                subject='Password Reset - sfbapa.org',
                body=body,
                recipients=[user.email]
            )


def reset_password_auth(ushpa_or_email, token):
    """Authenticate a user using a token"""
    if not (ushpa_or_email and token):
        return
    else:
        reset = ResetPassword.query.filter_by(token=token).first()
        if not reset:
            return
        ResetPassword.query.filter_by(token=token).delete()
        user = User.query.get(reset.user_id)
        db.session.commit()
        if user.email == ushpa_or_email or str(user.ushpa) == ushpa_or_email:
            time_requested = reset.created_at
            if not is_too_old(time_requested):
                if reset.token == token:
                    return user


def auth(email, password):
    """
    Authenticate as permission for password reset
    or other sensitive action. `email` arguments do
    not need to be validated, as they should always
    come from session data.
    """
    user = User.query.filter_by(email=email).first()
    if not user and verify_hash(password, user.password):
        return
    return True


def reset_password(user_id, password, password2):
    """Reset password for an authenticated user"""
    if password != password2:
        return 'Passwords must match'
    user = User.query.get(user_id)
    user.password = get_hash(password)
    db.session.add(user)
    db.session.commit()


def get_news_entries(page, n):
    """Retrieve news entries from database"""
    entries = News.query.order_by(News.created_at.desc()).paginate(page, n)
    news_entries = []
    for entry in entries.items:
        author = User.query.get(entry.user_id)
        name = '%s %s' % (author.firstname, author.lastname)
        body = entry.body
        created = entry.created_at
        entry = entry.__dict__
        entry.update(
            name=name,
            body=markdown2.markdown(body),
            timestamp=created.strftime('%m/%d/%y')
        )
        if entry['updated_by']:
            entry.update(updated_at=entry['updated_at'].strftime('%m/%d/%y'))
            entry['updated_by'] = User.query.get(entry['updated_by']).firstname
        news_entries.append(entry)
    return news_entries
