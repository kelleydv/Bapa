import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from bapa.utils import get_hash, timestamp, get_salt




class Base:

    def __init__(self):
        pass

    def init_db(self, db='bapa'):
        self.db = MongoClient()[db]
        return self

    def update(self, id, **kwargs):
        if isinstance(id, str):
            id = ObjectId(id)
        return self.collection.update(
            {'_id': id},
            {'$set': kwargs }
        )

    def from_id(self, id):
        if isinstance(id, str):
            id = ObjectId(id)
        return self.collection.find_one( {'_id':id} )

    def _ensure_ObjectIds(self, doc):
        return { k:ObjectId(v) for k,v in doc.items() if k.endswith('_id') and isinstance(v, str) }

    def match(self, **kwargs):
        #kwargs = self._ensure_ObjectIds(kwargs)
        return self.collection.find_one(kwargs)

    def match_all(self, **kwargs):
        return self.collection.find(kwargs)

    def latest(self, n=1, **kwargs):
        """
        Return the latest n documents matched by kwargs
        """
        kwargs = self._ensure_ObjectIds(kwargs)
        return [ x for x in self.collection.find(kwargs).sort('_id',-1)[0:n] ]
        





class User(Base):

    def __init__(self):
        self.init_db()
        self.collection = self.db.users

    def create(self, ushpa, email, password, firstname, lastname):
        salt = get_salt()
        return self.collection.insert({
            'ushpa': ushpa, # pilot number
            'email': email,
            'password': get_hash(password, salt),
            'salt': salt,
            'firstname': firstname,
            'lastname': lastname,
            'last_activity': timestamp(),
            'active': False,    # Is the user's membership active?
            'current': False,   # Has user paid membership dues?
            'officer': False,   # Is the user a BAPA officer?
            'admin': False,     # Does the user have admin priveleges?
        })

    def auth(self, ushpa, password):
        user = self.collection.find_one( {'ushpa':ushpa} )
        if user and get_hash(password, user['salt']) == user['password']:
            return user





class Account(Base):
    """
    For modeling user financial contributions
    """
    def __init__(self):
        self.init_db()
        self.collection = self.db.accounts

    def create(self, user_id, amount):
        return self.collection.insert({
            'user_id': user_id,
            'amount': amount,
            'date': timestamp(),
        })

    def from_user(self, user_id):
        return self.collection.find_one(
            {'user_id': user_id}
        )


