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
    created_at = db.Column(db.DateTime, default=lambda: timestamp(object=True))
    updated_at = db.Column(db.DateTime, onupdate=lambda: timestamp(object=True))
    updated_by = db.Column(db.Integer()) #user_id

    def __init__(self, user_id, subject, body, public):
        self.user_id = user_id
        self.subject = subject
        self.body = body
        self.public = public
        self.updated_by = None

    def __repr__(self):
        return '<News {} {} {}>'.format(self.user_id, self.subject, self.created_at)
