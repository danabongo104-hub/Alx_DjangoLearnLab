from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer
from rest_framework import filters
from rest_framework.exceptions import NotFound
# Create your views here.

# Implement a viewset for the Book model to handle CRUD operations
# ListAPIView for listing all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Must include these for filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering by Fields
    filterset_fields = ['author', 'title', 'publication_year']

    #Search
    search_fields = ['title', 'author']

    #Ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title'] #default


# RetrieveAPIView for retrieving a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# CreateAPIView for creating a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# UpdateAPIView for updating an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.request.data.get('pk')
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound(detail=f"Book with pk={pk} not found")
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.request.data.get('pk') or self.request.query_params.get('pk')
        if not pk:
            raise NotFound("Missing 'pk' for deleting book")
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound(f"Book with pk={pk} not found")