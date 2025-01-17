"""Books app views."""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from apps.books.models import BookModel
from apps.books.serializers import BookSerializer

class BooksViewSet(viewsets.ViewSet):
    """Books ViewSet.
    Contiene los servicios para la interaccion con la coleccion books."""
    @swagger_auto_schema(
        responses={200: BookSerializer(many=True)},
    )
    def list(self, request):
        """Lista todos los libros."""
        books = BookModel.all()
        serializer = BookSerializer(books, many=True)
        paginator = PageNumberPagination()
        paginated_books = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(paginated_books)

    @swagger_auto_schema(
        responses={
            201: BookSerializer,
            400: openapi.Response("Error en alguno de los campos.")
        },
    )
    def create(self, request):
        """Inserta un libro."""
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = BookModel(**serializer.validated_data)
            book.save()
            return Response(BookSerializer(book).data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        responses={
            200: BookSerializer,
            400: openapi.Response("Error en el id."),
            404: openapi.Response("No hay datos.")
        },
    )
    def retrieve(self, request, pk=None):
        """Obtiene un libro."""
        book = BookModel.get(pk)
        if not book:
            return Response({'error': 'Libro no encontrado.'}, status=404)
        return Response(BookSerializer(book).data)

    @swagger_auto_schema(
        responses={
            201: BookSerializer,
            400: openapi.Response("Error en el id o en los campos."),
            404: openapi.Response("No hay datos.")
        },
    )
    def update(self, request, pk=None):
        """Actualiza un libro."""
        book = BookModel.get(pk)
        if not book:
            return Response({'error': 'Libro no encontrado.'}, status=404)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            for key, value in serializer.validated_data.items():
                setattr(book, key, value)
            book.save()
            return Response(BookSerializer(book).data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        responses={
            204: openapi.Response("Sin contenido."),
            400: openapi.Response("Error en el id."),
            404: openapi.Response("No hay datos.")
        },
    )
    def destroy(self, request, pk=None):
        """Elimina un libro."""
        book = BookModel.get(pk)
        if not book:
            return Response({'error': 'Libro no encontrado.'}, status=404)
        book.delete()
        return Response(status=204)

    @swagger_auto_schema(
        responses={
            201: openapi.Response("Año consultado y precio promedio.",
                                  examples={
                                      "application/json": {
                                          'year': 2022, 
                                          'average_price': 30
                                        }
                                    }),
            400: openapi.Response("Error en el año."),
            404: openapi.Response("No hay datos.")
        },
    )
    @action(detail=False, methods=["get"], url_path="average-price")
    def average_price(self, request):
        """Obtiene el precio promedio segun el año indicado en parametros."""
        year = request.query_params.get("year")
        if not year or not year.isdigit():
            return Response(
                {'error': 'El parametro year es requerido y debe ser entero.'},
                status=400)
        year = int(year)
        average_price = BookModel.average_price_by_year(year)
        if average_price is not None:
            return Response({'year': year, 'average_price': average_price})
        return Response({'error': 'Datos no encontrados.'}, status=404)
