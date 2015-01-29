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

    def update(self, id, key, value):
        return self.collection.update(
            {'_id': ObjectId(id)},
            {'$set': {key:value}}
        )

    def from_id(self, id):
        if isinstance(id, str):
            id = ObjectId(id)
        return self.collection.find_one( {'_id':id} )


    def match(self, key, value):
        return self.collection.find_one( {key:value} )

    def match_all(self, key, value):
        return self.collection.find( {key:value} )





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

    def create(self, user_id, amount, date = timestamp()):
        return self.collection.insert({
            'user_id': user_id,
            'amount': amount,
            'date': date,
        })

    def from_user(self, user_id):
        return self.collection.find_one(
            {'user_id': user_id}
        )

