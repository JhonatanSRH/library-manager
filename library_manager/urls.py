"""URL configuration for library_manager project."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.books.urls')),
    path('docs/', include('library_manager.swagger')),
]
