from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_can_view, name='book_list'),
    path('books/create/', views.book_can_create, name='book_create'),
    path('books/<pk>/edit/', views.book_can_edit, name='book_edit'),
    path('books/<pk>/delete/', views.book_can_delete, name='book_delete'),
    path('form/', views.form_example, name='form_example'),
]
