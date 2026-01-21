from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('', list_books, name='home'), # home page shows all books
    path('books/', list_books, name='book-list'), # lists all books
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'), # detail view for a library
]