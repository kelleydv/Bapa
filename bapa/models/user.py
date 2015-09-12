from bapa.models import Base
from bapa.utils import get_hash, verify_hash, timestamp

class User(Base):

    collection = Base.db.users

    @classmethod
    def create(cls, ushpa, ushpa_data, email, password, firstname, lastname):
        return cls.collection.insert({
            'ushpa': ushpa, # pilot number
            'ushpa_data': ushpa_data, # from the USHPA API
            'email': email,
            'password': get_hash(password),
            'firstname': firstname,
            'lastname': lastname,
            'last_auth': timestamp()
        })

    @classmethod
    def auth(cls, ushpa, password):
        user = cls.collection.find_one({'ushpa': ushpa})
        if user and verify_hash(password, user['password']):
            cls.collection.update(
                {'_id': user['_id']},
                {
                    '$set': {'last_auth': timestamp()}
                }
            )
            return user
