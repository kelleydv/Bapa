import bapa.models as models
from bapa.utils import timestamp
from bapa import app
import requests

def record_user_activity(user_id):
    """
    Return True if last activity is successfully
    recorded in the database for user_id.
    """
    res = models.User.update(
                user_id,
                last_activity=timestamp()
            )
    if not res['updatedExisting']:
        return
    return True


def authenticate_user(ushpa, password):
    """
    Authenticate and return user document from
    database, None on failed auth.
    """
    return models.User.auth(ushpa, password)


def signup(ushpa, email, password, password2, firstname, lastname):
    """Register the user, return error or None."""
    ushpa_data = _get_ushpa_data(ushpa)
    if 'ERROR' in ushpa_data:
        error = 'You have to enter a valid ushpa number'
    elif not (email and '@' in email and '.' in email):
        error = 'You have to enter a valid email address'
    elif models.User.match(ushpa=ushpa):
        error = 'This USHPA pilot number is already in use by a current BAPA member'
    elif models.User.match(email=email):
        error = 'This email is already in use by a current BAPA member'
    elif not password:
        error = 'You have to enter a password'
    elif password != password2:
        error = 'The two passwords do not match'
    else:
        # Insert user into database.
        # See models.User for full schema
        models.User.create(
            ushpa,
            ushpa_data,
            email,
            password,
            firstname,
            lastname
        )
        return
    return error

def _get_ushpa_data(ushpa):
    """Access the USHPA API and return a dictionary of data"""
    req = 'https://www.ushpa.aero/ushpa_validation_ratings.asp?chapter=%s&pin=%s&ushpa=%s' 
    data = requests.get( req % (app.config['USHPA_CHAPTER'], app.config['USHPA_PIN'], ushpa) )
    #Parse plain text
    data = ( x for x in data.text.strip().split('\n') )
    data = ( x.split(':') for x in data )
    data = { k:v.strip() for k,v in data }
    return data
