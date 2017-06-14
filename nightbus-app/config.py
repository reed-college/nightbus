import os

class TestConfig:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'This is secret'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
#    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

