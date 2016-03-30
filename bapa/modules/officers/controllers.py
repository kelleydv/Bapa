from bapa import db
from bapa.models import Payment, User, News, Officer
from bapa.utils import is_too_old
import os

def _is_member(user_id):
    """
    Determine if someone is a member.
    If they have payed dues in the last year,
    they are a member.
    """
    dues = Payment.query.filter_by(user_id=user_id, item='Membership Dues').order_by(Payment.created_at.desc()).first()
    if dues:
        if not is_too_old(dues.created_at, years=1):
            return True
        return False


def get_members():
    """
    Return first name, last name, and rating
    for each registered user of the site.
    """
    users = User.query.all()
    f = lambda a: 'Active' if _is_member(a) else 'Not Active'
    users = [(x.firstname, x.lastname, x.ushpa_data.get('pg_pilot_rating'), f(x.id)) for x in users]
    return users

def news_update(subject, body, user_id):
    """
    Insert news entry into database
    """
    update = News(user_id, subject, body, True)
    db.session.add(update)
    db.session.commit()
    return update.id

def appoint(user_id, appointer_id, token=None):
    """
    Appoint an officer. Only officers can appoint officers,
    unless a token is used, which is stored as an environment
    variable. This allows for someone with access to the environment
    to appoint the first officer in the app. Be sure to use a
    long, cryptographically secure key, such as that provided by
    `bapa.utils.get_salt()`.
    """
    new_officer = User.query.get(user_id)
    if Officer.query.filter_by(user_id=user_id).first():
        return '%s %s is aready an officer.' % (new_officer.firstname, new_officer.lastname)
    success = '%s %s has been added as an officer.' % (new_officer.firstname, new_officer.lastname)
    if token:
        key = os.environ.get('APPOINTMENT_KEY')
        if key and key == token:
            officer = Officer(user_id, appointer_id)
            db.session.add(officer)
            db.session.commit()
            return success
    else:
        #check that the appointer_id is an officer
        if Officer.query.filter_by(user_id=appointer_id).first():
            officer = Officer(user_id, appointer_id)
            db.session.add(officer)
            db.session.commit()
            return success
    return 'Officer addition has failed.'
