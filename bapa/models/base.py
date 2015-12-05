import os
from pymongo import MongoClient
from bson.objectid import ObjectId

class Base:

    if os.environ.get('HEROKU'):
        uri = os.environ.get('MONGOLAB_URI')
        db = MongoClient(host=uri).get_default_database()
    else:
        db = MongoClient()['bapa']

    object_id = ObjectId # for use in subclasses

    @classmethod
    def update(cls, id, **kwargs):
        if isinstance(id, str):
            id = ObjectId(id)
        return cls.collection.update(
            {'_id': id},
            {'$set': kwargs}
        )

    @classmethod
    def from_id(cls, id):
        if isinstance(id, str):
            id = ObjectId(id)
        return cls.collection.find_one({'_id': id})

    @classmethod
    def match(cls, **kwargs):
        return cls.collection.find_one(kwargs)

    @classmethod
    def match_all(cls, **kwargs):
        return cls.collection.find(kwargs)

    @classmethod
    def latest(cls, n=1, **kwargs):
        """Return the latest n documents matched by kwargs"""
        return [x for x in cls.collection.find(kwargs).sort('_id', -1)[0:n]]

    @classmethod
    def paginate(cls, page=0, n=10):
        """
        Return a range of records suitable for pagination.
        skip() should not be used for larger data collections.
        """
        return [x for x in cls.collection.find().sort('_id', -1).limit(n).skip(page*n)]
