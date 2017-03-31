from bapa import db, app
from bapa.models import Payment, User, News, Officer
from bapa.utils import is_too_old, timestamp, parse_ratings
from bapa.services import send_email
from bapa.modules.membership.controllers import is_member
from apiclient import discovery
import os, json, string




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
    appointer = User.query.get(appointer_id)
    if Officer.query.filter_by(user_id=user_id).first():
        return '%s %s is aready an officer.' % (new_officer.firstname, new_officer.lastname)
    success = '%s %s has been added as an officer.' % (new_officer.firstname, new_officer.lastname)

    #appointer must be an officer, or use a key
    key = os.environ.get('APPOINTMENT_KEY')
    if (key and key == token) or Officer.query.filter_by(user_id=appointer_id).first():
        officer = Officer(user_id, appointer_id, office)
        db.session.add(officer)
        db.session.commit()

        #prepare email for other officers
        email_path = os.path.join(os.getcwd(), 'bapa', 'emails', 'appointment.txt')
        name = '%s %s' % (new_officer.firstname, new_officer.lastname)
        appointer = '%s %s' % (appointer.firstname, appointer.lastname)
        with open(email_path, 'r') as f:
            t = f.read()
            body = string.Template(t).substitute(appointer=appointer,
                new_officer=name, office=office, host=app.config['HOST'])

        send_email(
            subject='BAPA Officer Added',
            body=body,
            recipients=get_officer_emails()
        )
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
    unappointer = db.session.query(User).join(Officer, Officer.user_id==unappointer_id).first()
    if (key and key == token) or unappointer:
        db.session.delete(to_delete)
        db.session.commit()

        #prepare email for other officers
        email_path = os.path.join(os.getcwd(), 'bapa', 'emails', 'unappointment.txt')
        name = '%s %s' % (old_officer.firstname, old_officer.lastname)
        unappointer = '%s %s' % (unappointer.firstname, unappointer.lastname)
        with open(email_path, 'r') as f:
            t = f.read()
            body = string.Template(t).substitute(unappointer=unappointer,
                name=name, host=app.config['HOST'])

        send_email(
            subject='BAPA Officer Removed',
            body=body,
            recipients=get_officer_emails()
        )
        return success

    return 'Unappointment has failed.'

def get_member_emails():
    """
    Return a list of member emails. A member is someone who has payed dues within the last year.
    """
    emails = [x[0] for x in db.session.query(User.email).join(Officer, Officer.user_id==User.id).all()]
    return emails

def get_officers():
    """
    Return a list of officers.
    """
    officers = db.session.query(User.id, User.firstname, User.lastname, Officer.office).join(Officer, Officer.user_id==User.id)
    return officers

def get_officer_emails():
    """
    Return a list of officer emails.
    """
    emails = [x[0] for x in db.session.query(User.email).join(Officer, Officer.user_id==User.id).all()]
    return emails

def update_google_group(http_auth):
    """
    WIP: Update permissions on google group so that membership to group is
    based on club membership.

    Currently waiting for a google group email that can be accessed by the
    Admin SDK.
    """
    group_service = discovery.build('admin', 'directory_v1', http=http_auth)
    #print(app.config['GOOGLE_GROUP_EMAIL'])
    r = group_service.members().list(groupKey=app.config['GOOGLE_GROUP_EMAIL']).execute()
    #print(r)
    return None

def is_officer(user_id):
    """
    Return True or None.
    """
    if Officer.query.filter_by(user_id=user_id).first():
        return True
