from rest_framework import  generics, viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import ReadOnlyOrWrite

# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """ModelViewSet provides default implementations for CRUD operations
    Access is restricted to authenticated users only.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated,ReadOnlyOrWrite]