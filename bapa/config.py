import os

class Config():
    SECRET_KEY = 'ilovetofly'

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/bapa.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.dummy.com'
    MAIL_PORT = '123'
    MAIL_USERNAME = 'uname'
    MAIL_PASSWORD = 'pass'
    MAIL_DEFAULT_SENDER = 'awesome@awesome.com'

    USHPA_HOST = 'https://old.ushpa.aero'
    USHPA_CHAPTER = '1000'
    USHPA_PIN = '2000'

    HOST = 'http://localhost:5000'

class Debug(Config):
    DEBUG = True


class Develop(Debug):
    SECRET_KEY = os.environ.get('bapa_secret_key') or Config.SECRET_KEY

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI

    MAIL_SERVER = os.environ.get('bapa_mail_server')
    MAIL_PORT = os.environ.get('bapa_mail_port')
    MAIL_USERNAME = os.environ.get('bapa_mail_username')
    MAIL_PASSWORD = os.environ.get('bapa_mail_password')
    MAIL_DEFAULT_SENDER = os.environ.get('bapa_mail_default_sender')

    USHPA_CHAPTER = os.environ.get('bapa_ushpa_chapter')
    USHPA_PIN = os.environ.get('bapa_ushpa_pin')

    HOST = os.environ.get('bapa_host') or Config.HOST

    PAYPAL_ENDPOINT = 'https://www.sandbox.paypal.com/cgi-bin/webscr'

    #If PROTECTION is True, the app will implement google's reCAPTCHA
    PROTECTION = True
    RECAPTCHA_ENDPOINT = 'https://www.google.com/recaptcha/api/siteverify'
    RECAPTCHA_SECRET = os.environ.get('RECAPTCHA_SECRET')
    RECAPTCHA_SITEKEY = os.environ.get('RECAPTCHA_SITEKEY')
    #https://developers.google.com/recaptcha/intro

class Testing(Develop):
    TESTING = True #to avoid sending emails
    PROTECTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test-bapa.db'
