from django import forms
from .models import Book

#se crea la clase bookForm de forms para poder crear formularios con fácilidad
#solo se debe indicar el modelo, que en este caso es book, y los campos que queremos
#que se muestren en el formulario
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'stock']