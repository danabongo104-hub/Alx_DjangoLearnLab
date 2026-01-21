from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.shortcuts import render
from .models import Book
from .models import Library
# Create your views here.
# function based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# class based view to list all libraries
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


    
