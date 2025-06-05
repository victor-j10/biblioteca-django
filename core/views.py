from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Book, User, History
from django.urls import reverse_lazy
from .forms import BookForm
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

# Create your views here.

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class BookListView(ListView):
    model = Book
    template_name = 'core/libro_list.html'
    context_object_name = 'books'
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'core/libro_detail.html'
    context_object_name = 'book'

class BookCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'core/book_form.html'
    success_url = reverse_lazy('libro_list')
    
class BookUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'core/book_form.html'
    success_url = reverse_lazy('libro_list')

def regular_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'regular':
            return view_func(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para acceder a esta vista.")
        return redirect('lista_libros')
    return _wrapped_view

@method_decorator([login_required, regular_required], name='dispatch')
class BorrowReturnBookView(View):
    def get(self, request):
        books = Book.objects.all()
        borrowed = request.user.borrowed_books.all()
        context = {
            'books': books,
            'borrowed_books': borrowed,
            
        }
        return render(request, 'core/borrow_books.html', context)
    
    def post(self, request):
        action = request.POST.get('action')
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        
        if action == 'borrow':
            if book.stock > 0 and book not in request.user.borrowed_books.all():
                request.user.borrowed_books.add(book)
                book.stock -= 1
                history = History(
                user = request.user,
                book = book,
                borrowed_at = datetime.now())
                history.save()
                book.save()
                messages.success(request, f'Has tomado prestado"{book.title}".')
            else:
                messages.error(request, 'No puedes tomar este libro.')
        
        elif action == 'return':
            if book in request.user.borrowed_books.all():
                request.user.borrowed_books.remove(book)
                book.stock += 1
                book.save()
                
                latest_entry = History.objects.filter(user=request.user, book=book, returned_at__isnull=True).last()
                if latest_entry:
                    latest_entry.returned_at = datetime.now()
                    latest_entry.save()
                messages.success(request, f'Has devuelto"{book.title}".')
            else:
                messages.error(request, 'No tienes este libro.')
        return redirect('borrow-books')
    
@method_decorator([login_required, regular_required], name='dispatch')
class BorrowHistoryView(View):
    def get(self, request):
        history_entries = History.objects.filter(user=request.user).order_by('-borrowed_at')
        context = {
            'history': history_entries
        }
        return render(request, 'core/history.html', context)
                