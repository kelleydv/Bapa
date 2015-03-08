import bapa.models as models

def get_last_payment(user_id):
    """Retrieve latest payment info for user, or return None"""
    latest = models.Payment.latest( user_id=user_id )
    if latest:
        return latest[0]
    return

def make_payment(ushpa, password, amount):
    """
    Authenticate and record user payment.  Return error string
    on failure.
    """
    user = models.User.auth(ushpa, password)
    if not user:
        return "Invalid password"
    else:
        models.Payment.create(user['_id'], amount)
        return