from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import (
    BookListApiView, 
    BookDetailAPIView,
    BookCreateAPIView,
    BookUpdateAPIView,
    BookDeleteAPIView,
    BorrowBookAPIView, 
    ReturnBookAPIView
    )

urlpatterns = [
    path('books/', BookListApiView.as_view(), name='api-book-list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='api-book-detail'),
    path('books/create/',BookCreateAPIView.as_view(), name='api-book-create'),
    path('books/<int:pk>/update/', BookUpdateAPIView.as_view(), name='api-book-update'),
    path('books/<int:pk>/delete/', BookDeleteAPIView.as_view(), name='api-book-delete'),
    path('api-token-auth/', obtain_auth_token),
    path('books/borrow/', BorrowBookAPIView.as_view(), name='api-borrow-book'),
    path('books/return/', ReturnBookAPIView.as_view(), name='api-return-book'),
    
]