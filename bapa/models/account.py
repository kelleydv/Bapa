from bapa.utils import timestamp
from bapa.models import Base

class Account(Base):
    """For modeling user financial contributions"""
    
    collection = Base.db.accounts

    @classmethod
    def create(cls, user_id, amount):
        return cls.collection.insert({
            'user_id': user_id,
            'amount': amount,
            'date': timestamp(),
        })

    @classmethod
    def from_user(cls, user_id):
        return cls.collection.find_one(
            {'user_id': user_id}
        )

