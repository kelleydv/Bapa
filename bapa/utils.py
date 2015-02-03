from passlib.hash import pbkdf2_sha256
import datetime
import os
from base64 import b64decode, b64encode

def get_hash(m):
    """
    One hundred thousand applications of sha256
    """
    return pbkdf2_sha256.encrypt(m, salt_size=64, rounds=100000)

def verify_hash(password, hash):
    """Verify and return boolean"""
    return pbkdf2_sha256.verify(password, hash)

def get_salt():
    """return a salt string"""
    return b64encode(os.urandom(64)).decode('utf-8')

def timestamp():
    return str(datetime.datetime.utcnow())
