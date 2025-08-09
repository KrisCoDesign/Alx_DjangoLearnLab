from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Book, Author
from django.contrib.auth import get_user_model


class BookTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('testuser', 'test@gmail.com', 'password')
        self.client.force_authenticate(user=self.user)

    def test_create_acount(self):
        url = reverse('book_create')
        self.author = Author.objects.create(name='Test Author')
        data = {
            'title': 'Test Book ApiRequest', 
            'publication_year': 2022, 
            'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(Book.objects.get().title, 'Test Book ApiRequest')

    def test_update_book(self):
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(title="1984", author=self.author, publication_year=1949)
        url = reverse('book_update', args=[self.book.id])
        data = {
            'title': 'Test Book ApiRequest', 
            'publication_year': 2022, 
            'author': self.author.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book ApiRequest')

    def text_delete_book(self):
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(title="1984", author=self.author, publication_year=1949)
        url = reverse('book_delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)