from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
# Roles de los usuarios
ROLES = (
    ('regular', 'Usuario Regular'),
    ('admin', 'Administrador'),
)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} - {self.author}"

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default='regular')
    borrowed_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.name 

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.book} ({'Devuelto' if self.returned_at else 'Prestado'})"
    


