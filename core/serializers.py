from rest_framework import serializers
from .models import Book

#se indica que se obtendran siempre todos los campos del modelo book para las consultas a la api
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'