import os 
from datetime import timedelta 

class Config:

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'RefugeesRegistration.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Suppress warning
    SECRET_KEY = 'thisisasecretkeyforsomereasonidonotlikeatall'
    CORS_ORIGINS = ["http://localhost:3000"] # Adjust if your frontend runs on a different port/domain
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300