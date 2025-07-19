from django.urls import path
from . import views
from .views import list_books


urlpatterns = [
    path('templates/', views.list_books, name='list_books'),
    path('templates/', views.LibraryDetailView.as_view(), name='library_detail')                          
]
