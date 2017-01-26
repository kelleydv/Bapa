from bapa import app, mail
from flask_mail import Message
import os

def send_email(subject=None, body=None, recipients=None):
    """Send an email"""

    msg = Message(
        subject=subject,
        body=body,
        recipients=recipients
    )

    if app.config['TESTING']:
        #no need to send an email
        return
    elif app.debug and not os.environ.get('HEROKU'):
        #print to the terminal, copy/paste url
        print('to: %s' % recipients)
        print('subject: %s' % subject)
        print('body:\n%s' % body)
    else:
        #send the email
        with app.app_context():
            mail.send(msg)
