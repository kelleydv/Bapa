from bapa import db
from bapa.utils import timestamp

class Payment(db.Model):
    """For modeling user financial contributions"""

    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    item = db.Column(db.String())
    amount = db.Column(db.Float())
    date = db.Column(db.String())
    #TODO: Parse paypal date for datetime object
    created_at = db.Column(db.DateTime, default=lambda:timestamp(object=True))
    ipn_id = db.Column(db.Integer())

    def __init__(self, user_id, item, amount, date, ipn_id):
        self.user_id = user_id
        self.item = item
        self.amount = amount
        self.date = date
        self.ipn_id = ipn_id

    def __repr__(self):
        return '<Payment {} {} {} {} {}>'.format(self.id, self.user_id,
                            self.item, self.amount, self.date)
