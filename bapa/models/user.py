from bapa import db
from bapa.utils import get_hash, timestamp
from sqlalchemy import PickleType

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    ushpa = db.Column(db.Integer)
    ushpa_data = db.Column(PickleType)
    email = db.Column(db.String())
    password = db.Column(db.String())
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    last_login = db.Column(db.DateTime, default=lambda: timestamp(object=True))
    created_at = db.Column(db.DateTime, default=lambda: timestamp(object=True))
    updated_at = db.Column(db.DateTime, default=lambda: timestamp(object=True),
                           onupdate=lambda: timestamp(object=True))

    def __init__(self, ushpa, ushpa_data, email, password, firstname, lastname):
        self.ushpa = ushpa
        self.ushpa_data = ushpa_data
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return '<User {} {} {}>'.format(self.id, self.ushpa, self.email)
