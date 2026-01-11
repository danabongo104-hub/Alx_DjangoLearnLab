# CRUD Operations for Book Model
# Create

from bookshelf.models import Book

# Create a book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()
book

# The Book instance is successfully created and saved to the database.
# No error is returned, and the object now exists in the Book table.

# Verification
Book.objects.all()
# <QuerySet [<Book: 1984>]>
