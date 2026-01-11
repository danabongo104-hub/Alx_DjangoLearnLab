from bookshelf.models import Book

# retrieve a book
Book.objects.get(title="1984")

# retriev all books
Book.objects.all()

# <!-- expected output -->
# <!-- <QuerySet [<Book: Book object (1)> -->

# retrieve books with id(1)
Book.objects.filter(id=1)
# <!-- expected output -->
# <!-- <QuerySet [<Book: Book object (1)>]> -->
