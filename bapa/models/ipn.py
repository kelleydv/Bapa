from bapa import db
from bapa.utils import timestamp

class Ipn(db.Model):
    """Paypal IPNs"""

    __tablename__ = 'ipns'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    ipn = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=lambda: timestamp(object=True))

    def __init__(self, user_id, ipn):
        self.user_id = user_id
        self.ipn = ipn

    def __repr__(self):
        return '<IPN {} {} {}>'.format(self.id, self.user_id, self.ipn)
