import os

class Config:
    DEBUG = False
    TESTING = False
    MONGO_URI = "mongodb://localhost:27017/presupuesto"
    SECRET_KEY = '1qaz2wsxtatan'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True