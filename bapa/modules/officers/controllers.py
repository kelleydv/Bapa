from bapa import db, app
from bapa.models import Payment, User, News, Officer
from bapa.utils import is_too_old, timestamp, parse_ratings
from bapa.modules.membership.controllers import is_member
import os, json




def get_members():
    """
    Return id, first name, last name, and rating
    for each registered user of the site.
    """
    users = User.query.all()
    f = lambda a: 'Active' if is_member(a) else 'Not Active'
    users = [(x.id, x.firstname, x.lastname, 3,
        parse_ratings(x.ushpa_data), f(x.id)) for x in users]
    return users

def news_update(subject, body, user_id, news_id=None):
    """
    Insert news entry into database. If a news_id is provided,
    update that record in the database.
    """
    if news_id:
        update = News.query.filter_by(id=news_id).first()
        update.subject = subject
        update.body = body
        update.updated_by = user_id
        update.updated_at = timestamp(object=True)
    else:
        update = News(user_id, subject, body, True)
        db.session.add(update)
    db.session.commit()
    return update.id

def get_news(id):
    """
    Return the subject and body of a news update
    """
    post = News.query.filter_by(id=id).first()
    if post:
        return post.subject, post.body


def delete_news(id):
    """"
    Delete a news update from the db
    """
    News.query.filter_by(id=id).delete()
    db.session.commit()

def appoint(user_id, appointer_id, office, token=None):
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

    #appointer must be an officer, or use a key
    key = os.environ.get('APPOINTMENT_KEY')
    if (key and key == token) or Officer.query.filter_by(user_id=appointer_id).first():
        officer = Officer(user_id, appointer_id, office)
        db.session.add(officer)
        db.session.commit()
        return success
    return 'Officer addition has failed.'


def unappoint(user_id, unappointer_id, token=None):
    """
    Unappoint an officer. Only officers can unappoint officers, unless a token is ussed.
    """

    old_officer = User.query.get(user_id)
    to_delete = Officer.query.filter_by(user_id=user_id).first()
    if not to_delete:
        return '%s %s is not an officer.' % (old_officer.firstname, old_officer.lastname)

    #unappointer must be an officer, or be using a key
    success = '%s %s has been unappointed as an officer.' % (old_officer.firstname, old_officer.lastname)
    key = os.environ.get('APPOINTMENT_KEY')
    if (key and key == token) or Officer.query.filter_by(user_id=unappointer_id).first():
        db.session.delete(to_delete)
        db.session.commit()
        return success

    return 'Unappointment has failed.'


def get_officers():
    """
    Return a list of officers.
    """
    officers = db.session.query(User.id, User.firstname, User.lastname, Officer.office).join(Officer, Officer.user_id==User.id)
    return officers

def is_officer(user_id):
    """
    Return True or False.
    """
    if Officer.query.filter_by(user_id=user_id).first():
        return True
    return False

#Use this function in the interface!!
app.jinja_env.globals.update(is_officer=is_officer)
