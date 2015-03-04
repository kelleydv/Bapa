import os
from pymongo import MongoClient
from bson.objectid import ObjectId

class Base:

    db = MongoClient()['bapa']

    @classmethod
    def update(cls, id, **kwargs):
        if isinstance(id, str):
            id = ObjectId(id)
        return cls.collection.update(
            {'_id': id},
            {'$set': kwargs }
        )

    @classmethod
    def from_id(cls, id):
        if isinstance(id, str):
            id = ObjectId(id)
        return cls.collection.find_one( {'_id':id} )

    @staticmethod
    def _ensure_ObjectIds(doc):
        return { k:ObjectId(v) for k,v in doc.items() if k.endswith('_id') and isinstance(v, str) }

    @classmethod
    def match(cls, **kwargs):
        return cls.collection.find_one(kwargs)

    @classmethod
    def match_all(cls, **kwargs):
        return cls.collection.find(kwargs)

    @classmethod
    def latest(cls, n=1, **kwargs):
        """Return the latest n documents matched by kwargs"""
        kwargs = cls._ensure_ObjectIds(kwargs)
        return [ x for x in cls.collection.find(kwargs).sort('_id',-1)[0:n] ]
