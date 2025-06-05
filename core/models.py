from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
# se dejan instanciados los nombres de los roles disponibles
ROLES = (
    ('regular', 'Usuario Regular'),
    ('admin', 'Administrador'),
)

#se crea la clase book
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} - {self.author}"

#se crea la clase user
class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default='regular')
    borrowed_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.name 

#se crea la clase historial
class History(models.Model):
    #llave foranea para relacionar history con user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #llave foranea para relacionar history con book
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.book} ({'Devuelto' if self.returned_at else 'Prestado'})"
    


