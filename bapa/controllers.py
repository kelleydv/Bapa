from bapa import models
from bapa.utils import timestamp

def record_user_activity(user_id):
    """
    Return True if last activity is successfully
    recorded in the database for user_id.
    """
    res = models.User().update(
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
    return models.User().auth(ushpa, password)


def signup(ushpa, email, password, password2, firstname, lastname):
    """Register the user, return error or None."""
    if not (ushpa and len(ushpa) is 5):
        error = 'You have to enter a valid ushpa number'
    elif not (email and '@' in email and '.' in email):
        error = 'You have to enter a valid email address'
    elif models.User().match(ushpa=ushpa):
        error = 'This USHPA pilot number is already in use by a current BAPA member'
    elif models.User().match(email=email):
        error = 'This email is already in use by a current BAPA member'
    elif not password:
        error = 'You have to enter a password'
    elif password != password2:
        error = 'The two passwords do not match'
    else:
        # Insert user into database.
        # See models.User for full schema
        models.User().create(
            ushpa,
            email,
            password,
            firstname,
            lastname
        )
        return
    return error

def get_last_payment(user_id):
    """Retrieve latest payment info for user, or return None"""
    return models.Account().latest( user_id=user_id )[0]

def make_payment(ushpa, password, amount):
    """
    Authenticate and record user payment.  Return error string
    on failure.
    """
    user = models.User().auth(ushpa, password)
    if not user:
        return "Invalid password"
    else:
        models.Account().create(user['_id'], amount)
        return
