from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from .models import Book, History
from .serializers import BookSerializer

#se crea el metodo para obtener el listado de los libros
class BookListApiView(generics.ListAPIView):
    #se envía la query
    queryset = Book.objects.all()
    #se indica el serializer
    serializer_class = BookSerializer
    
class BookDetailAPIView(generics.RetrieveAPIView):
    queryset =Book.objects.all()
    serializer_class = BookSerializer

#se crea el metodo para validar que el usuario sea un admin
class IsAdminUserCustom(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
#se crea el metodo para validar que el usuario sea regular
class IsRegularUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'regular'

class BookCreateAPIView(generics.CreateAPIView):
    queryset =Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUserCustom]
    
class BookUpdateAPIView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserCustom]
    
class BookDeleteAPIView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserCustom]
    
#se crea la clase para prestar un libro
class BorrowBookAPIView(APIView):
    #se válida que el usuario sea regular
    permission_classes = [IsRegularUser]
    
    #método para prestar libros
    def post(self, request):
        #se obtiene el id de la solicitud
        book_id = request.data.get('book_id')
        #se busca una coincidencia
        book = get_object_or_404(Book, id=book_id)
        
        #si el stock es menor o igual a cero se indica que no quedan libros disponibles
        if book.stock <= 0:
            return Response({'error': 'No hay stock disponible para este libro.'}, status=status.HTTP_400_BAD_REQUEST)
        
        #si el libro ya está reservado se indica que no se puede volver a reservar
        if book in request.user.borrowed_books.all():
            return Response({'error': 'Ya tienes este libro reservado.'}, status=status.HTTP_BAD_REQUEST)
        
        #en dado caso lo anterior no se cumpla se añade el libro a la reserva
        request.user.borrowed_books.add(book)
        #se disminuye el stock
        book.stock -= 1
        #se guarda el nuevo valor del stock
        book.save()
        
        #se crea el historial
        History.objects.create(user=request.user, book=book, borrowed_at=datetime.now())
        
        return Response({'message': f'Has tomado prestado "{book.title}"'}, status=status.HTTP_200_OK)
    
#se crea la clase para devolcer un libro
class ReturnBookAPIView(APIView):
    #se válida que el usuario sea regular
    permission_classes = [IsRegularUser]
    
    #se crea la función
    def post(self, request):
        #se obtiene el id del libro en la solicitud
        book_id = request.data.get('book_id')
        #se busca una coincidencia en la bd
        book = get_object_or_404(Book, id=book_id)
        
        #se valida que el libro exista en la reservación, si no se le informará que aún no lo reserva
        if book not in request.user.borrowed_books.all():
            return Response({'error': 'No tienes este libro'}, status=status.HTTP_400_BAD_REQUEST)
        
        #se elimina el libro de la reservación del usuario
        request.user.borrowed_books.remove(book)
        #se vuelve a sumar al stock del libro
        book.stock += 1
        #se guarda el nuevo valor
        book.save()
        
        #se busca el último registro del libro dónde la fecha de return sea nula
        history = History.objects.filter(user=request.user, book=book, returned_at__isnull=True).last()
        #si la encuentra, crea la fecha en la que se devolvió y se guarda el valor.
        if history:
            history.returned_at = datetime.now()
            history.save()
        
        return Response({'message': f'Has devuelto "{book.title}"'}, status=status.HTTP_200_OK)