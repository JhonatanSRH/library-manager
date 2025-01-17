"""Books app tests."""
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from pymongo.collection import ObjectId

class BookAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Configuración inicial antes de todas las pruebas."""
        # Conexión a MongoDB
        cls.client = settings.MONGO_CLIENT
        cls.db = cls.client['LIBRARY-TEST']
        cls.collection = cls.db['books']
        # Datos iniciales
        cls.data = [
            {
                "_id": ObjectId("6789b5fbabf068ca1dc63f75"),
                "title": "La Divina Comedia",
                "author": "Dante Alighieri",
                "published_date": datetime(1321, 9, 1),
                "genre": "TEST",
                "price": 31.49
            },
            {
                "_id": ObjectId("6789b5fbabf068ca1dc83f05"),
                "title": "Hamlet",
                "author": "William Shakespeare",
                "published_date": datetime(1321, 1, 1),
                "genre": "TEST",
                "price": 24.49
            }
        ]
        cls.collection.insert_many(cls.data)
        # Crear un usuario para las pruebas
        cls.user = User.objects.create_user(username='testuser', 
                                            password='password123')
        cls.token = Token.objects.create(user=cls.user)

    @classmethod
    def tearDownClass(cls):
        """Limpia los datos después de todas las pruebas."""
        cls.collection.delete_many({})
        cls.client.close()

    def setUp(self):
        """Autentica el cliente con el token del usuario de pruebas"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_books(self):
        """Prueba listar libros."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data['count'], len(self.data))

    def test_retrieve_book(self):
        """Prueba obtener un libro."""
        book_id = self.data[0]['_id']
        response = self.client.get(f'/api/books/{book_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.data[0]['title'])
    
    def test_average_price(self):
        """Prueba calcular el precio promedio de libros por año."""
        year = self.data[0]['published_date'].year
        avg_price = sum((self.data[0]['price'],
                         self.data[1]['price'])) / len(self.data)
        response = self.client.get(f'/api/books/average-price/?year={year}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['average_price'], avg_price)

    def test_error_average_price(self):
        """Prueba error al calcular el precio promedio de libros por año."""
        year = self.data[0]['published_date'].year-1000
        response = self.client.get(f'/api/books/average-price/?year={year}')
        self.assertEqual(response.status_code, 404)

    def test_create_book(self):
        """Prueba crear un libro."""
        new_book = {
            "title": "Test Book",
            "author": "Autor 3",
            "published_date": "2023-01-01",
            "genre": "Fantasia",
            "price": 20.99
        }
        response = self.client.post('/api/books/', new_book, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], new_book['title'])

    def test_update_book(self):
        """Prueba actualizar un libro."""
        book_id = self.data[1]['_id']
        updated_data = {
            "title": self.data[1]['title'] + " Test Book",
            "author": self.data[1]['author'],
            "published_date": str(self.data[1]['published_date']),
            "genre": self.data[1]['genre'],
            "price": self.data[1]['price'],
        }
        response = self.client.put(f'/api/books/{book_id}/', updated_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], updated_data['title'])

    def test_delete_book(self):
        """Prueba eliminar un libro."""
        new_book = {
            "title": "Test Book",
            "author": self.data[1]['author'],
            "published_date": self.data[1]['published_date'],
            "genre": self.data[1]['genre'],
            "price": self.data[1]['price'],
        }
        res_post = self.client.post('/api/books/', new_book, format='json')
        response = self.client.delete(f"/api/books/{res_post.data['_id']}/")
        self.assertEqual(response.status_code, 204)
