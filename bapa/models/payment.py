from bapa.models import Base
from bapa.utils import timestamp

class Payment(Base):
    """For modeling user financial contributions"""

    collection = Base.db.payments

    @classmethod
    def create(cls, user_id, item, amount, date, ipn_id):
        return cls.collection.insert({
            'user_id': cls.object_id(user_id),
            'item': item, # Dues, donation, etc.
            'amount': amount,
            'date': date,
            'timestamp': timestamp(), # todo: parse paypal date for datetime obj
            'ipn_id': ipn_id # passed as ObjectId
        })
