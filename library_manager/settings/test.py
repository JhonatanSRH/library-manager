"""dev settings."""
from library_manager.settings.base import *
from pymongo import MongoClient

MONGO_CLIENT = MongoClient(env('MONGO_URI'))
MONGO_DB = env('MONGO_DB') + '-TEST'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
