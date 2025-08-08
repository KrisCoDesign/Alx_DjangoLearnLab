from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
# from .views import BookCreateView
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
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book ApiRequest')
