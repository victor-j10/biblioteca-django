from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BorrowReturnBookView,
    BorrowHistoryView
)

urlpatterns = [
    path('', BookListView.as_view(), name='libro_list'),
    path('libros/<int:pk>/', BookDetailView.as_view(), name='libro_detail'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('libros/crear/', BookCreateView.as_view(), name='libro_create'),
    path('libros/<int:pk>/actualizar', BookUpdateView.as_view(), name='libro_editar'),
    path('borrow/', BorrowReturnBookView.as_view(), name='borrow-books'),
    path('history/', BorrowHistoryView.as_view(), name='borrow-history'),
]
