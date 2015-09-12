from bapa.models import Base

class Ipn(Base):
    """Paypal IPNs"""

    collection = Base.db.ipns

    @classmethod
    def create(cls, user_id, ipn):
        return cls.collection.insert({
            'user_id': cls.object_id(user_id),
            'ipn': ipn
        })
