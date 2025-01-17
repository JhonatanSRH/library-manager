"""Books apps config."""
from django.apps import AppConfig

class BooksConfig(AppConfig):
    """Book App Config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.books'
