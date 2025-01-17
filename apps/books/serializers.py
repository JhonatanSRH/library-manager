"""Books app serializers"""
from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    """Book Serializer"""
    _id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    published_date = serializers.DateTimeField(format="%Y-%m-%d")
    genre = serializers.CharField(max_length=100)
    price = serializers.FloatField()
