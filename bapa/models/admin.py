from bapa import db
from bapa.utils import timestamp

class Admin(db.Model):
    """Website administrators"""

    __tablename__ = 'administrators'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    appointer_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, default=lambda: timestamp(object=True))

    def __init__(self, user_id, appointer_id):
        self.user_id = user_id
        self.appointer_id = appointer_id

    def __repr__(self):
        return '<Administrator {}>'.format(self.user_id)
