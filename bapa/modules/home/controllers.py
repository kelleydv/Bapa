from bapa import app, mail, db, services
from bapa.models import User, ResetPassword, Officer, Admin, News, Payment
from bapa.utils import is_too_old
from bapa.utils import get_salt, get_hash, verify_hash
from flask_mail import Message
import markdown2
import string
import os


def authenticate_user(ushpa, password):
    """
    Authenticate and return user record from
    database, None on failed auth.  Prepare for
    use as session data.
    """
    user = User.query.filter_by(ushpa=ushpa).first()
    if not (user and verify_hash(password, user.password)):
        return
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


def signup(ushpa, email, password, password2, firstname, lastname):
    """Register the user, return error or None."""
    if not (email and '@' in email and '.' in email):
        error = 'You have to enter a valid email address'
    elif User.query.filter_by(ushpa=ushpa).first():
        error = 'This USHPA pilot number is already in use by a current BAPA member'
    elif User.query.filter_by(email=email).first():
        error = 'This email is already in use by a current BAPA member'
    elif not password:
        error = 'You have to enter a password'
    elif password != password2:
        error = 'The two passwords do not match'
    else:
        # Insert user into database.
        ushpa_data = services.ushpa.get_pilot_data(ushpa)
        user = User(
            ushpa,
            ushpa_data,
            email,
            password,
            firstname,
            lastname
        )
        db.session.add(user)
        db.session.commit()
        return
    return error


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

            if app.config['TESTING']:
                return
            elif app.debug and not os.environ.get('HEROKU'):
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
        db.session.commit()
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
        time = entry.created_at
        entry = entry.__dict__
        entry.update(
            name=name,
            body=markdown2.markdown(body),
            timestamp=time.strftime('%b %d, %Y')
        )
        entry.update()
        news_entries.append(entry)
    return news_entries
