"""Mongo models"""
from bson import errors
from django.conf import settings
from pymongo.collection import ObjectId
from rest_framework.validators import ValidationError

MONGO_DB = settings.MONGO_CLIENT[settings.MONGO_DB]

error_messages = {
    'validation': 'Este %s tiene un formato invalido.'
}

class MongoModel:
    """Mongo Model.
    Representacion de una coleccion de MongoDB como un objeto Python."""
    collection_name = None  # Nombre de la colección en MongoDB

    @classmethod
    def collection(cls):
        """Obtiene el objeto coleccion."""
        if not cls.collection_name:
            raise ValueError("Debe definir 'collection_name' en el modelo.")
        return MONGO_DB[cls.collection_name]

    @classmethod
    def all(cls):
        """Obtiene todos los documentos de la coleccion."""
        return [cls(**doc) for doc in cls.collection().find()]

    @classmethod
    def get(cls, _id):
        """Obtiene un documento teniendo en cuenta su _id."""
        try:
            doc = cls.collection().find_one({'_id': ObjectId(_id)})
            if doc:
                return cls(**doc)
        except errors.InvalidId:
            raise ValidationError(
                {'_id': error_messages['validation'] % '_id'})
        return None

    @classmethod
    def filter(cls, **kwargs):
        """Hace el filtro de los documentos."""
        return [cls(**doc) for doc in cls.collection().find(kwargs)]

    def __init__(self, **kwargs):
        """Inicializa todos los atributos del modelo."""
        self._id = str(kwargs.get('_id')) if '_id' in kwargs else None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """Guarda o actualiza el documento."""
        data = self.to_dict()
        if self._id:
            # Actualizar documento existente
            try:
                self.collection().update_one(
                    {'_id': ObjectId(self._id)},
                    {'$set': data}
                )
            except errors.InvalidId:
                raise ValidationError(
                    {'_id': error_messages['validation'] % '_id'})
        else:
            # Insertar nuevo documento
            result = self.collection().insert_one(data)
            self._id = str(result.inserted_id)

    def delete(self):
        """Elimina el documento basado en el _id."""
        if self._id:
            try:
                self.collection().delete_one({'_id': ObjectId(self._id)})
                self._id = None
            except errors.InvalidId:
                raise ValidationError(
                    {'_id': error_messages['validation'] % '_id'})

    def to_dict(self):
        """Convierte la instancia a un diccionario para ser guardada."""
        data = {}
        for key, value in self.__dict__.copy().items():
            if key == '_id' and value is None:
                continue
            else:
                data[key] = value
        return data
