from django.urls import path
from . import views


urlpatterns = [
    path('book/', views.book_view, name='book')
    path('library/', views.LibraryDetailView.as_view(), name='library')                          
]
