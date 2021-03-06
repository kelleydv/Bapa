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
    SECRET_KEY = os.environ.get('SECRET_KEY', Config.SECRET_KEY)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', Config.SQLALCHEMY_DATABASE_URI)

    MAIL_SERVER = os.environ.get('SENDGRID_SMTP_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = "apikey"
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    USHPA_CHAPTER = os.environ.get('USHPA_CHAPTER')
    USHPA_PIN = os.environ.get('USHPA_PIN')

    HOST = os.environ.get('HOST', Config.HOST)

    PAYPAL = {
        'domain': 'https://www.sandbox.paypal.com',
        'endpoint': 'https://www.sandbox.paypal.com/cgi-bin/webscr',
        'button_id': os.environ.get('PAYPAL_BUTTON_ID'),
        'donate_button_id': os.environ.get('PAYPAL_DONATE_BUTTON_ID')
    }



    #If RECAPTCHA is True, the app will implement google's reCAPTCHA
    RECAPTCHA = True
    RECAPTCHA_ENDPOINT = 'https://www.google.com/recaptcha/api/siteverify'
    RECAPTCHA_SECRET = os.environ.get('RECAPTCHA_SECRET')
    RECAPTCHA_SITEKEY = os.environ.get('RECAPTCHA_SITEKEY')
    #https://developers.google.com/recaptcha/intro

    #For integrating Google Calendar with fullcalendar
    GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
    GOOGLE_CAL_ID=os.environ.get('GOOGLE_CAL_ID')

    #Google Analytics
    GA_TRACKING_ID = os.environ.get('GA_TRACKING_ID')

    #profile pictures
    CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

class Testing(Develop):
    TESTING = True #to avoid sending emails
    RECAPTCHA = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////var/tmp/test-bapa.db'

class Production(Develop):
    DEBUG = False
    PAYPAL = {
        'domain': 'https://www.paypal.com',
        'endpoint': 'https://www.paypal.com/cgi-bin/webscr',
        'button_id': os.environ.get('PAYPAL_BUTTON_ID')
    }
