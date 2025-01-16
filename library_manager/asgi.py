"""ASGI config for library_manager project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_manager.settings.dev')

application = get_asgi_application()
