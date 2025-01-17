"""Add books command"""
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Añade datos a la coleccion books"""
    help = 'Añade 5 documentos a la coleccion de libros'

    def handle(self, *args, **kwargs):
        """Inserta 5 documentos en la coleccion books"""
        # Configuracion de la conexion a MongoDB
        db = settings.MONGO_CLIENT[settings.MONGO_DB]
        books_collection = db['books']
        # Datos a insertar
        books = [
            {
                "title": "Moby-Dick",
                "author": "Herman Melville",
                "published_date": datetime(1851, 11, 14),
                "genre": "Novela",
                "price": 19.99
            },
            {
                "title": "100 Años de soledad",
                "author": "Gabriel Garcia Marquez",
                "published_date": datetime(1967, 5, 21),
                "genre": "Novela",
                "price": 14.99
            },
            {
                "title": "La Divina Comedia",
                "author": "Dante Alighieri",
                "published_date": datetime(1321, 9, 1),
                "genre": "Epopeya",
                "price": 31.49
            },
            {
                "title": "Hamlet",
                "author": "William Shakespeare",
                "published_date": datetime(1603, 1, 1),
                "genre": "Drama",
                "price": 24.49
            },
            {
                "title": "Frankenstein",
                "author": "Mary Shelley",
                "published_date": datetime(1818, 1, 1),
                "genre": "Épico",
                "price": 22.99
            },
        ]
        # Inserta los libros en la coleccion
        result = books_collection.insert_many(books)
        self.stdout.write(
            self.style.SUCCESS(
                f'Agregados {len(result.inserted_ids)} datos a la coleccion'))
