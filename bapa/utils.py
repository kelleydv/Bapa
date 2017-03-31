from passlib.hash import pbkdf2_sha256
from dateutil.parser import parse
import secrets
import datetime



def get_hash(m):
    """One hundred thousand applications of sha256"""
    return pbkdf2_sha256.using(salt_size=64, rounds=100000).hash(m)

def verify_hash(password, hash):
    """Verify and return boolean"""
    try:
        return pbkdf2_sha256.verify(password, hash)
    except:
        # In the case of a DB record that is not a valid
        # pbkdf2_sha256 hash, such as with migrated data
        return False

def get_salt():
    """Return a salt string"""
    return secrets.token_hex(64)

def timestamp(object=False):
    """Return a timestamp as an object or a string"""
    if not object:
        return str(datetime.datetime.utcnow())
    else:
        return datetime.datetime.utcnow()

def object_from_timestamp(date_str):
    """Create an object from a timestamp string"""
    return parse(date_str)

def is_too_old(time_obj, minutes=5, years=0):
    """Return True if a timestamp is older than limit, False otherwise"""
    if not time_obj:
        return True
    elapsed = datetime.datetime.utcnow() - time_obj
    if elapsed > datetime.timedelta(minutes=minutes, days=years*365):
        return True
    return False

def parse_ratings(ushpa_data):
    """
    Parse ushpa data from bapa.services.ushpa.get_pilot_data
    to return a string such as 'P2, H3'.
    """
    rating_dict = {
        'BEGINNER': '1',
        'NOVICE': '2',
        'INTERMEDIATE': '3',
        'ADVANCED': '4',
        'MASTER': '5'
    }

    pg = ushpa_data.get('pg_pilot_rating')
    hg = ushpa_data.get('hg_pilot_rating')
    ratings = ''
    if pg:
        ratings += 'P-%s' % rating_dict[pg]
    if hg:
        ratings += ' H-%s' % rating_dict[hg]
    if ratings:
        return ratings.strip()
    return
