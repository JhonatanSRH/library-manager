"""WSGI config for library_manager project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_manager.settings.dev')

application = get_wsgi_application()
