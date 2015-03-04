from bapa.models import Base
from bapa.utils import get_salt, timestamp

class ResetPassword(Base):
    """Records inserted when a user requests a password reset"""

    collection = Base.db.resets

    @classmethod
    def create(cls, user_id, timestamp, secret):
        return cls.collection.insert({
            'user_id': user_id,
            'timestamp': timestamp,
            'secret': secret
        })

    @classmethod
    def delete(cls, secret):
        cls.collection.remove( {'secret':secret} )
