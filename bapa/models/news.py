from bapa import db
from bapa.utils import timestamp

class News(db.Model):
    """For modeling news entries"""

    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    subject = db.Column(db.String())
    body = db.Column(db.String())
    public = db.Column(db.Boolean()) #public vs. members only
    created_at = db.Column(db.DateTime, default=lambda:timestamp(object=True))

    def __init__(self, user_id, subject, body, public):
        self.user_id = user_id
        self.subject = subject
        self.body = body
        self.public = public

    def __repr__(self):
        return '<News {} {} {}>'.format(self.user_id, self.subject, self.created_at)
