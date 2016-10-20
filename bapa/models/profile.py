
from bapa import db
from bapa.utils import timestamp


class Profile(db.Model):
    """
    Extra user Data
    """

    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    private = db.Column(db.Boolean)
    joindate = db.Column(db.DateTime)
    nickname = db.Column(db.String)
    callsign = db.Column(db.String)
    sites = db.Column(db.String)
    website = db.Column(db.String)
    company = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.Integer)
    country = db.Column(db.String)
    cellphone = db.Column(db.Integer)
    landphone = db.Column(db.Integer)
    prophone = db.Column(db.Integer)
    emergency_contact = db.Column(db.String)
    emergency_phone = db.Column(db.Integer)
    wing_info = db.Column(db.String)


    created_at = db.Column(db.DateTime, default=lambda: timestamp(object=True))
    updated_at = db.Column(db.DateTime, default=lambda: timestamp(object=True),
                           onupdate=lambda: timestamp(object=True))

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<Profile {} {}>'.format(self.id, self.user_id)
