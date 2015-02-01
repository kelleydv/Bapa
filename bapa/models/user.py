from bapa.models import Base
from bapa.utils import get_hash, get_salt, timestamp

class User(Base):

    def __init__(self):
        self.init_db()
        self.collection = self.db.users

    def create(self, ushpa, email, password, firstname, lastname):
        salt = get_salt()
        return self.collection.insert({
            'ushpa': ushpa, # pilot number
            'email': email,
            'password': get_hash(password, salt),
            'salt': salt,
            'firstname': firstname,
            'lastname': lastname,
            'last_activity': timestamp(),
            'active': False,    # Is the user's membership active?
            'current': False,   # Has user paid membership dues?
            'officer': False,   # Is the user a BAPA officer?
            'admin': False,     # Does the user have admin priveleges?
        })

    def auth(self, ushpa, password):
        user = self.collection.find_one( {'ushpa':ushpa} )
        if user and get_hash(password, user['salt']) == user['password']:
            return user
