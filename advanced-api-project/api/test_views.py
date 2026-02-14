"""
/api/test_views.py

Unit tests for the Book API endpoints in advanced-api-project.

Tests cover:
- CRUD operations (Create, Read, Update, Delete)
- Filtering, searching, and ordering
- Permissions and authentication
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Author


class TestBookAPIEndpoints(APITestCase):
    """Test suite for the Book API endpoints."""

    def setUp(self):
        """Set up test user, author, and books."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name='Jenn Hastins')

        self.book1 = Book.objects.create(title='Crime', author=self.author, publication_year=2020)
        self.book2 = Book.objects.create(title='Mystery', author=self.author, publication_year=2021)

        self.client = APIClient()

    # ---------------------------
    # CRUD Tests
    # ---------------------------

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Crime')

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-create')
        data = {'title': 'New Book', 'author': self.author.pk, 'publication_year': 2022}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {'title': 'New Book', 'author': self.author.pk, 'publication_year': 2022}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-update')
        data = {'pk':self.book1.pk,'title': 'Crime Updated', 'author': self.author.pk, 'publication_year': 2020}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Crime Updated')

    def test_update_book_unauthenticated(self):
        url = reverse('book-update')
        data = {'pk':self.book1.pk,'title': 'Crime Hack', 'author': self.author.pk, 'publication_year': 2020}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-delete')
        data = {'pk': self.book1.pk}
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        url = reverse('book-delete')
        data = {'pk': self.book1.pk}
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # ---------------------------
    # Filtering, Searching, Ordering
    # ---------------------------

    def test_filter_books_by_author(self):
        url = reverse('book-list') + f'?author={self.author.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_books_by_title(self):
        url = reverse('book-list') + '?search=Crime'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Crime')

    def test_order_books_by_title(self):
        Book.objects.create(title='A Book', author=self.author, publication_year=1950)
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'A Book')