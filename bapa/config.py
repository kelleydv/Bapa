import os

class Config():
    SECRET_KEY = 'ilovetofly'

    MAIL_SERVER = 'smtp.dummy.com'
    MAIL_PORT = '123'
    MAIL_USERNAME = 'uname'
    MAIL_PASSWORD = 'pass'
    MAIL_DEFAULT_SENDER = 'awesome@awesome.com'

    USHPA_HOST = 'https://www.ushpa.aero'
    USHPA_CHAPTER = '1000'
    USHPA_PIN = '2000'

class Debug(Config):
    DEBUG = True


class Develop(Debug):
    SECRET_KEY = os.environ.get('bapa_secret_key')

    MAIL_SERVER = os.environ.get('bapa_mail_server')
    MAIL_PORT = os.environ.get('bapa_mail_port')
    MAIL_USERNAME = os.environ.get('bapa_mail_username')
    MAIL_PASSWORD = os.environ.get('bapa_mail_password')
    MAIL_DEFAULT_SENDER = os.environ.get('bapa_mail_default_sender')

    USHPA_CHAPTER = os.environ.get('bapa_ushpa_chapter')
    USHPA_PIN = os.environ.get('bapa_ushap_pin')

    PAYPAL_ENDPOINT = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
