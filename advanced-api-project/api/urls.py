from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('books/', BookListView.as_View(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_View(), name='book-detail'),
    path('books/create/', BookCreateView.as_View(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_View(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_View(), name='book-delete'),
]