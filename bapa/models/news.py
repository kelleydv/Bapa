from bapa.models import Base
from bapa.utils import timestamp

class News(Base):
    """For modeling news entries"""

    collection = Base.db.news

    @classmethod
    def create(cls, user_id, subject, body):
        print('herro')
        return cls.collection.insert({
            'user_id': cls.object_id(user_id),
            'subject': subject,
            'body': body,
            'public': True, # public vs. members only
            'timestamp': timestamp(),
        })
