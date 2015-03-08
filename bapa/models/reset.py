from bapa.models import Base
from bapa.utils import get_salt, timestamp

class ResetPassword(Base):
    """Records inserted when a user requests a password reset"""

    collection = Base.db.resets

    @classmethod
    def create(cls, user_id, timestamp, token):
        return cls.collection.insert({
            'user_id': user_id,
            'timestamp': timestamp,
            'token': token
        })

    @classmethod
    def delete(cls, token):
        cls.collection.remove( {'token':token} )
