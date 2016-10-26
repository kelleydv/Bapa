import os

class Config():
    SECRET_KEY = 'ilovetofly'

    SQLALCHEMY_DATABASE_URI = 'sqlite:////var/tmp/bapa.db'
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
    SECRET_KEY = os.environ.get('SECRET_KEY') or Config.SECRET_KEY

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    USHPA_CHAPTER = os.environ.get('USHPA_CHAPTER')
    USHPA_PIN = os.environ.get('USHPA_PIN')

    HOST = os.environ.get('HOST') or Config.HOST

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
    SQLALCHEMY_DATABASE_URI = 'sqlite:////var/tmp/test-bapa.db'
