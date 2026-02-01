from django.urls import path

from relationship_app import member_view, librarian_view, admin_view
from django.contrib.auth.views import LoginView,LogoutView
from .views import delete_book,add_book,edit_book, list_books, LibraryDetailView
from . import views

urlpatterns = [
    path('', list_books, name='home'), # home page shows all books
    path('books/', list_books, name='book-list'), # lists all books
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'), # detail view for a library
    # authentication paths
    #authentication views url
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'), 
    
    # Role-based URLs
    path('admin-page/', admin_view.admin_view, name='admin-page'),
    path('librarian-page/', librarian_view.librarian_view, name='librarian-page'),
    path('member-page/', member_view.member_view, name='member-page'),
    
   # Custom permission URLs (checker-friendly)
path('add_book/', add_book, name='add-book'),
path('edit_book/<int:pk>/', edit_book, name='edit-book'),
path('delete_book/<int:pk>/', delete_book, name='delete-book'),





]