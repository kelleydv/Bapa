from bapa import db
from bapa.utils import timestamp

class Officer(db.Model):
    """Club officers"""

    __tablename__ = "officers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    appointer_id = db.Column(db.Integer())
    office = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=lambda: timestamp(object=True))

    def __init__(self, user_id, appointer_id, office):
        self.user_id = user_id
        self.appointer_id = appointer_id
        self.office = office

    def __repr__(self):
        return '<Officer {}>'.format(self.user_id)
