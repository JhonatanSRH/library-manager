"""Books app urls."""
from rest_framework.routers import DefaultRouter
from apps.books.views import BooksViewSet

router = DefaultRouter()

router.register(r'books', BooksViewSet, basename='book')

urlpatterns = router.urls