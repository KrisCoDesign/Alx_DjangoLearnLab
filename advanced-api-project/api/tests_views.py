from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from .views import BookCreateView
from .models import Book, Author
from django.contrib.auth import get_user_model


class BookTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user('testuser', 'test@gmail.com', 'password')
        self.author = Author.objects.create(name='Test Author')

    def test_create_book(self):
        data = {'title': 'Test Book ApiRequest', 
                'publication_year': 2022, 
                'author': self.author.id}
        request = self.factory.post('/api/books/', data, format='json')
        force_authenticate(request, user=self.user)
        response = BookCreateView.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book ApiRequest')

