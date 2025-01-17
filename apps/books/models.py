"""Books app models."""
from datetime import datetime
from mongo.models import MongoModel

class BookModel(MongoModel):
    """Book Model Collection."""
    collection_name = "books"

    def __init__(self, title: str, author: str, published_date: datetime, 
                 genre: str, price: float, _id=None):
        """Inicializa los campos que tiene la coleccion"""
        super().__init__(_id=_id, title=title, author=author, 
                         published_date=published_date, 
                         genre=genre, price=price)

    @classmethod
    def average_price_by_year(cls, year):
        """
        Calcula el precio promedio de los libros publicados en un año especifico.
        """
        pipeline = [
            {
                "$match": {
                    "published_date": {
                        "$gte": datetime(year, 1, 1),
                        "$lt": datetime(year + 1, 1, 1)
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "average_price": {"$avg": "$price"}
                }
            }
        ]
        result = list(cls.collection().aggregate(pipeline))
        return result[0]["average_price"] if result else None
