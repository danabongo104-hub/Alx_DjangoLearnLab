#CRUD Operations for Book Model
#Create

from books.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()

# The Book instance is successfully created and saved to the database.
# No error is returned, and the object now exists in the Book table.

# Verification
Book.objects.all()
# <QuerySet [<Book: 1984>]>
