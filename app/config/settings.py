class Settings:
    APP_NAME = "API Embrapa"
    DEBUG = True
    JWT_SECRET_KEY = 'embrapa_fiap_mlet_giacang'
    JWT_ALGORITHM = "HS256"
    JWT_EXP_DELTA_SECONDS = 3600
    BEARER_PREFIX = "Bearer "
    
    USERNAME = "embrapa_fiap_mlet_giacang"
    PASSWORD = "1234"
    SECRET_KEY = 'embrapa_fiap_mlet_giacang'
    CACHE_TYPE = 'simple'
    SWAGGER = {
        'title' :'Catalogo de Embrapa - Projeto MLET',
        'uiversion' : 3
    }
    SQLALCHEMY_DATABASE_URI = 'sqlite:///embrapa.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
 