class Config(object):
    DEBUG = False
    TESTING = False
    
    SECRET_KEY = "ELfmKjhDfoV09yzayQhVIPHpf9fMuoV1"
    
    DB_NAME = 'production-db'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'example'
       
    SESSION_COOKIE_SECURE = True
    
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    
    DB_NAME = 'dev-db'
    DB_USERNAME = 'dev'
    DB_PASSWORD = 'example'
    
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    DEBUG = False
    Testing = True
    
    SESSION_COOKIE_SECURE = False
        
