from bapa import db
from bapa.utils import timestamp

class ResetPassword(db.Model):
    """Records inserted when a user requests a password reset"""

    __tablename__ = 'resets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    token = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=lambda: timestamp(object=True))

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def __repr__(self):
        return '<Reset {} {}>'.format(self.user_id, self.created_at)
