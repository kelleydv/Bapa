from passlib.hash import pbkdf2_sha256
import datetime
import os
from base64 import b64decode, b64encode
import binascii

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
    salt = b64encode(os.urandom(64))
    return binascii.hexlify(salt).decode('utf-8')

def timestamp(object = False):
    if not object:
        return str(datetime.datetime.utcnow())
    else:
        return datetime.datetime.utcnow()

def object_from_timestamp(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
