from bapa import models

def get_members():
    """
    Return first name, last name, and rating
    for each registered user of the site.
    """
    users =  models.User.match_all()
    members = [(x['firstname'], x['lastname'], x['ushpa_data'].get('pg_pilot_rating')) for x in users]
    return members
