import os
from pymongo import MongoClient
from bson.objectid import ObjectId

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
