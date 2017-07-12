import local_config

class TestConfig:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = local_config.SECRET_KEY
    MAIL_SERVER = local_config.MAIL_SERVER
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = local_config.MAIL_USERNAME
    MAIL_PASSWORD = local_config.MAIL_PASSWORD
