from bapa.models import Base
from bapa.utils import timestamp

class Ipn(Base):
    """Paypal IPNs"""

    collection = Base.db.ipns

    @classmethod
    def create(cls, user_id, ipn):
        return cls.collection.insert({
            'user_id': user_id,
            'ipn': ipn
        })

    @classmethod
    def from_user(cls, user_id):
        return cls.collection.find_one(
            {'user_id': user_id}
        )
