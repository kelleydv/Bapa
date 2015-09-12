from bapa import models
from bapa.utils import object_from_timestamp, is_too_old

def _is_member(id):
    dues = models.Payment.latest(user_id=id, item='Membership Dues')
    if dues:
        t = object_from_timestamp(dues[0]['timestamp'])
        if not is_too_old(t, years=1):
            return True
        return False


def get_members():
    """
    Return first name, last name, and rating
    for each registered user of the site.
    """
    users = models.User.match_all()
    f = lambda a: 'Active' if _is_member(a) else 'Not Active'
    members = [(x['firstname'], x['lastname'], x['ushpa_data'].get('pg_pilot_rating'), f(x['_id'])) for x in users]
    return members
