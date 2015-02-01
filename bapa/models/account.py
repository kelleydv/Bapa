from bapa.utils import timestamp
from bapa.models import Base

class Account(Base):
    """
    For modeling user financial contributions
    """
    def __init__(self):
        self.init_db()
        self.collection = self.db.accounts

    def create(self, user_id, amount):
        return self.collection.insert({
            'user_id': user_id,
            'amount': amount,
            'date': timestamp(),
        })

    def from_user(self, user_id):
        return self.collection.find_one(
            {'user_id': user_id}
        )

