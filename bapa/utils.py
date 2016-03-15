from passlib.hash import pbkdf2_sha256
from base64 import b64encode
import datetime
import os
import binascii

def get_hash(m):
    """One hundred thousand applications of sha256"""
    return pbkdf2_sha256.encrypt(m, salt_size=64, rounds=100000)

def verify_hash(password, hash):
    """Verify and return boolean"""
    return pbkdf2_sha256.verify(password, hash)

def get_salt():
    """Return a salt string"""
    salt = b64encode(os.urandom(64))
    return binascii.hexlify(salt).decode('utf-8')

def timestamp(object=False):
    """Return a timestamp as an object or a string"""
    if not object:
        return str(datetime.datetime.utcnow())
    else:
        return datetime.datetime.utcnow()

def object_from_timestamp(date_str):
    """Create an object from a timestamp string"""
    return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

def is_too_old(time_obj, minutes=5, years=0):
    """Return True if a timestamp is older than limit, False otherwise"""
    if not time_obj:
        return True
    elapsed = datetime.datetime.utcnow() - time_obj
    if elapsed > datetime.timedelta(minutes=minutes, days=years*365):
        return True
    return False
