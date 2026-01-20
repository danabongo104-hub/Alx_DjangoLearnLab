from relationship_app.models import Author, Book, Library, Librarian

#samples
#create instances of models since in the last task we deleted them

# Create Authors
author1 = Author.objects.create(name="Hally Jackson")
author2 = Author.objects.create(name="Jennifer Twain")

# Create Books
book1 = Book.objects.create(title = "As Good As Dead", author=author1)
book2 = Book.objects.create(title = "The Missing Girl", author=author2)
book3 = Book.objects.create(title = "Gone Girls", author=author1)

# Create Libraries
library1 = Library.objects.create(name="harambee Library")
library1.books.set([book1, book2]) # to show many-to-many relationship
library2 = Library.objects.create(name="National Library")

#Create Librarians
librarian1 = Librarian.objects.create(name="Roy Mwangi", library=library1)
librarian2 = Librarian.objects.create(name="Alice Wanjiku", library=library2)   

#Query Samples
#1.Query all books by a specific author.
# hally_books = Book.objects.filter(author__name="Hally Jackson")
# print("These are by Hally Jackson:",list(hally_books))

# jenny_books = Book.objects.filter(author__name="Jennifer Twain")
# print("These are by Jennifer Twain:",jenny_books)
# Query all books by a specific author
author_name = "Hally Jackson"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
print("Books by", author.name + ":", list(books_by_author))


#2. List all books in a library.
# buruburu_books = library1.books.all()
# print("Books in Buruburu Library:", list(buruburu_books))
#retriev a library by name
library_name = "Buruburu Library"
buruburu_library = Library.objects.get(name=library_name)
print("Library Retrieved:", buruburu_library.name)
#its books
print("Books in", library_name + ":", list(buruburu_library.books.all()))

# 3. Retrieve the librarian for a library.
# buruburu_librarian = library1.librarian
# Retrieve the librarian for a library by querying
buruburu_librarian = Librarian.objects.get(library=library1)
print("Librarian of Buruburu Library:", buruburu_librarian.name)
print("Librarian Retrieved:", buruburu_librarian.name)