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
            'last_activity': timestamp(),
            'active': False,    # Is the user's membership active?
            'current': False,   # Has user paid membership dues?
            'officer': False,   # Is the user a BAPA officer?
            'admin': False,     # Does the user have admin priveleges?
        })

    @classmethod
    def auth(cls, ushpa, password):
        user = cls.collection.find_one( {'ushpa':ushpa} )
        if user and verify_hash(password, user['password']):
            return user
