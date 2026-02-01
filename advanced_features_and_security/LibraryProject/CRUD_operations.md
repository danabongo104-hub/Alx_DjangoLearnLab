from bookshelf.models import Book

# create a book instance
book = Book(title = "1984", author = "George Orwell",publication_year = 1949) 
book.save() 

# Get the book and update the title
book = Book.objects.get(title="1984") book.title = "Nineteen Eighty-Four" 
book.save()

# retrieve all books
Book.objects.all()

# retrieve books with id(1)
Book.objects.filter(id=1)

# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four") 
book.delete()

# Confirm deletion
Book.objects.all()