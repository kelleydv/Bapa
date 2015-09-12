from bapa.models import Base

class Officer(Base):
    """Club officers"""

    collection = Base.db.officers

    @classmethod
    def create(cls, user_id):
        return cls.collection.insert({
            'user_id': cls.object_id(user_id)
        })
