import hashlib
import datetime
import os
from base64 import b64decode, b64encode

def get_hash(m, salt = None):
    """one hundred thousand applications of sha256"""
    if salt:
        m = salt + m
    for x in range(100000):
        m = hashlib.sha256(m.encode('utf-8')).hexdigest()
    
    return m

def get_salt():
    """return a salt string"""
    return b64encode(os.urandom(64)).decode('utf-8')

def timestamp():
    return str(datetime.datetime.utcnow())
