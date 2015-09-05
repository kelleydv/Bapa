from bapa import models
from bapa import app, services
from bapa.utils import timestamp


def authenticate_user(ushpa, password):
    """
    Authenticate and return user document from
    database, None on failed auth.  Prepare for
    use as session data.
    """
    user = models.User.auth(ushpa, password)
    if not user:
        return
    user['_id'] = str(user['_id'])
    if models.Officer.match(user_id=user['_id']):
        user['officer'] = True
    if models.Admin.match(user_id=user['_id']):
        user['admin'] = True
    return user


def signup(ushpa, email, password, password2, firstname, lastname):
    """Register the user, return error or None."""
    ushpa_data = services.ushpa.get_pilot_data(ushpa)
    #if 'ERROR' in ushpa_data:
    #    error = 'You have to enter a valid ushpa number'
    if not (email and '@' in email and '.' in email):
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
