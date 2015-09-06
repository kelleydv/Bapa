from bapa.models import Base
from bapa.utils import timestamp

class Ipn(Base):
    """Paypal IPNs"""

    collection = Base.db.ipns

    @classmethod
    def create(cls, user_id, ipn):
        return cls.collection.insert({
            'user_id': cls.object_id(user_id),
            'ipn': ipn
        })
