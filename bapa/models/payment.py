from bapa.models import Base
from bapa.utils import timestamp

class Payment(Base):
    """For modeling user financial contributions"""
    
    collection = Base.db.payments

    @classmethod
    def create(cls, user_id, amount):
        return cls.collection.insert({
            'user_id': user_id,
            'amount': amount,
            'date': timestamp(),
        })

    @classmethod
    def from_user(cls, user_id):
        return cls.latest(user_id=user_id)

