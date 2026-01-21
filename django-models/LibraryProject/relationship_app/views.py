from django.shortcuts import render
from django.views.generic import DetailView
from django.shortcuts import render
from .models import Book, Library
# Create your views here.
# function based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# class based view to list all libraries
class LibraryListView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


    
