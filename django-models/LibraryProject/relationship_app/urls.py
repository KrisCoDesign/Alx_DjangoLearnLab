from django.urls import path
from . import views


urlpatterns = [
    path('relationship_app/', views.book_view, name='book_books')
    path('relationship_app/', views.LibraryDetailView.as_view(), name='library_detail')                          
]
