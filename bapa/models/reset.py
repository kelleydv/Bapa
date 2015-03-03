from bapa.models import Base
from bapa.utils import get_salt, timestamp

class Reset(Base):
    """Records inserted when a user requests a password reset"""

    def __init__(self):
        self.init_db()
        self.collection = self.db.resets

    def create(self, user_id, timestamp, secret):
        return self.collection.insert({
            'user_id': user_id,
            'timestamp': timestamp,
            'secret': secret
        })

    def delete(self, secret):
        user = self.collection.remove( {'secret':secret} )
