from bookshelf.models import Book

# Get the book and update the title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
<!-- ouput -->
<!-- <Book: Book object (1)> -->