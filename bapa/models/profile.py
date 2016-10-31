
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
    prophone = db.Column(db.String)
    proemail = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.String)
    country = db.Column(db.String)
    cellphone = db.Column(db.String)
    landphone = db.Column(db.String)
    emergency_contact = db.Column(db.String)
    emergency_phone = db.Column(db.String)
    wing_info = db.Column(db.String)

    delorme = db.Column(db.String)
    linkedin = db.Column(db.String)
    facebook = db.Column(db.String)
    instagram = db.Column(db.String)
    twitter = db.Column(db.String)
    google = db.Column(db.String)
    github = db.Column(db.String)
    youtube = db.Column(db.String)
    vimeo = db.Column(db.String)
    soundcloud = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=lambda: timestamp(object=True))
    updated_at = db.Column(db.DateTime, default=lambda: timestamp(object=True),
                           onupdate=lambda: timestamp(object=True))

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<Profile {} {}>'.format(self.id, self.user_id)
