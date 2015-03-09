from bapa.models import Base
from bapa.utils import timestamp

class Administrator(Base):
    """A record of an admin"""
    
    collection = Base.db.administrators

    @classmethod
    def create(cls, user_id, appointer_id, office):
        return cls.collection.insert({
            'user_id': user_id,
            'appointer_id': appointer_id,
            'date': timestamp(),
        })

    @classmethod
    def from_user(cls, user_id):
        return cls.collection.find_one(
            {'user_id': user_id}
        )

    @classmethod
    def delete(cls, id):
        return cls.collection.remove(
            {'_id': id}
        )

