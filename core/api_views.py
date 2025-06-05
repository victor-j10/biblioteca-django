from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from .models import Book, History
from .serializers import BookSerializer

class BookListApiView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class BookDetailAPIView(generics.RetrieveAPIView):
    queryset =Book.objects.all()
    serializer_class = BookSerializer

class IsAdminUserCustom(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
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
    
class BorrowBookAPIView(APIView):
    permission_classes = [IsRegularUser]
    
    def post(self, request):
        book_id = request.data.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        
        if book.stock <= 0:
            return Response({'error': 'No hay stock disponible para este libro.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if book in request.user.borrowed_books.all():
            return Response({'error': 'Ya tienes este libro reservado.'}, status=status.HTTP_BAD_REQUEST)
        
        request.user.borrowed_books.add(book)
        book.stock -= 1
        book.save()
        
        History.objects.create(user=request.user, book=book, borrowed_at=datetime.now())
        
        return Response({'message': f'Has tomado prestado "{book.title}"'}, status=status.HTTP_200_OK)
    
class ReturnBookAPIView(APIView):
    permission_classes = [IsRegularUser]
    
    def post(self, request):
        book_id = request.data.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        
        if book not in request.user.borrowed_books.all():
            return Response({'error': 'No tienes este libro'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.borrowed_books.remove(book)
        book.stock += 1
        book.save()
        
        history = History.objects.filter(user=request.user, book=book, returned_at__isnull=True).last()
        if history:
            history.returned_at = datetime.now()
            history.save()
        
        return Response({'message': f'Has devuelto "{book.title}"'}, status=status.HTTP_200_OK)