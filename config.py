import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///invms.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = REDIS_URL
    SWAGGER = {
    'title': 'Inventory API',
    'uiversion': 3
    }


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False


config_map = {
'development': DevConfig,
'production': ProdConfig,
}