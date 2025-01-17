"""dev settings."""
from library_manager.settings.base import *
from pymongo import MongoClient

MONGO_CLIENT = MongoClient(env('MONGO_URI'))

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
