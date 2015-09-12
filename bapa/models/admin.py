from bapa.models import Base

class Admin(Base):
    """Website administrators"""

    collection = Base.db.administrators

    @classmethod
    def create(cls, user_id):
        return cls.collection.insert({
            'user_id': cls.object_id(user_id)
        })
