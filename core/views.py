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
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

class BookListView(LoginRequiredMixin, ListView):
    """ 
    Método para mostrar los libros disponibles. Se agregó la validación de que solo permita acceder
    cuando el usuario está logueado. 
    """
    model = Book
    template_name = 'core/libro_list.html'
    context_object_name = 'books'
    login_url = 'login'
    
class BookDetailView(LoginRequiredMixin, DetailView):
    """ 
    Método para mostrar el detalle de un libro seleccionado. 
    Se agregó la validación de que solo permita acceder cuando el usuario está logueado. 
    """
    model = Book
    template_name = 'core/libro_detail.html'
    context_object_name = 'book'
    login_url = 'login'

class BookCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """ 
    Método para crear un libro (solo admin). 
    Se agregó la validación de que solo permita acceder cuando el usuario está logueado y que sea
    administrador. Adicional, también se redirecciona a la lista de libros una vez se complete
    la creación.
    """
    model = Book
    form_class = BookForm
    template_name = 'core/book_form.html'
    success_url = reverse_lazy('libro_list')
    
class BookUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """ 
    Método para actualizar un libro (solo admin). 
    Se agregó la validación de que solo permita acceder cuando el usuario está logueado y que sea
    administrador. Adicional, también se redirecciona a la lista de libros una vez se complete
    la creación.
    """
    model = Book
    form_class = BookForm
    template_name = 'core/book_form.html'
    success_url = reverse_lazy('libro_list')

def regular_required(view_func):
    """ 
    Método para validar que el usuario sea un usuario regular. 
    """
    def _wrapped_view(request, *args, **kwargs):
        #se valida que el usuario esté autenticado y que el rol sea "regular"
        if request.user.is_authenticated and request.user.role == 'regular':
            #si es verdadero se deja pasar
            return view_func(request, *args, **kwargs)
        #si es falso se le informa que no tiene permiso y se redirecciona a la vista raíz.
        messages.error(request, "No tienes permiso para acceder a esta vista.")
        return redirect('/')
    return _wrapped_view


#se agregó el decorador para indicar a este metodo que solo puede ser usuado si:
#1. está logueado. 2. es un usuario regular
@method_decorator([login_required, regular_required], name='dispatch')
class BorrowReturnBookView(View):
    """ 
    Método para obtener los libros
    """
    def get(self, request):
        #se obtienen todos los libros de la bd
        books = Book.objects.all()
        #se obtiene todos los libros reservados por el usuario
        borrowed = request.user.borrowed_books.all()
        #se crea el contexto para poder utilizarlos en la vista
        context = {
            'books': books,
            'borrowed_books': borrowed,
            
        }
        return render(request, 'core/borrow_books.html', context)
    
    """ 
    Método para prestar un libro
    """
    def post(self, request):
        #se obtiene la acción hecha por el usuario "borrow" --> prestar, "return" --> devolver
        action = request.POST.get('action')
        #se obtiene el id del libro
        book_id = request.POST.get('book_id')
        #se compara el id del libro de arriba con el id de los libros en la bd
        #si hay una coincidencia se obtienen todos sus datos
        book = get_object_or_404(Book, id=book_id)
        
        #si la acción es borrow se ingresa al método
        if action == 'borrow':
            #si el stock es mayor a cero y el libro seleccionado no está reservado
            if book.stock > 0 and book not in request.user.borrowed_books.all():
                #se añade el libro al usuario
                request.user.borrowed_books.add(book)
                #se disminuye el stock del libro
                book.stock -= 1
                #se crea el historial de la reservación
                history = History(
                user = request.user,
                book = book,
                borrowed_at = datetime.now())
                #se guarda el historial en la bd
                history.save()
                #se guarda el nuevo valor del stock del libro en la bd
                book.save()
                messages.success(request, f'Has tomado prestado"{book.title}".')
            else:
                messages.error(request, 'No puedes tomar este libro.')
        
        #si la acción es "return"
        elif action == 'return':
            #se valida que el libro esté en todas las reservaciones del usuario
            if book in request.user.borrowed_books.all():
                #se elimina el libro de las reservaciónes
                request.user.borrowed_books.remove(book)
                #se vuelve a actualizar el stock del libro
                book.stock += 1
                #se guarda el nuevo valor del stock en la bd
                book.save()
                
                #se obtiene la última entrada del libro en el historial
                latest_entry = History.objects.filter(user=request.user, book=book, returned_at__isnull=True).last()
                #si la obtiene
                if latest_entry:
                    #se crea la fecha del retorno
                    latest_entry.returned_at = datetime.now()
                    #se guarda esa fecha en el historial
                    latest_entry.save()
                messages.success(request, f'Has devuelto"{book.title}".')
            else:
                messages.error(request, 'No tienes este libro.')
        return redirect('borrow-books')

#se añade el decorador para indicar que este método solo puede ser accesible cuando
#1. se está logueado, 2. el usuario es regular    
@method_decorator([login_required, regular_required], name='dispatch')
class BorrowHistoryView(View):
    """ 
    Método para obtener el historial del usuario
    """
    def get(self, request):
        #se obtienen todos el historial del usuario en sesión y se ordenan por la decga reservada
        history_entries = History.objects.filter(user=request.user).order_by('-borrowed_at')
        #se crea el contexto para luego ser usado en la vista
        context = {
            'history': history_entries
        }
        return render(request, 'core/history.html', context)
                