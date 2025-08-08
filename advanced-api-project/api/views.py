
from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filter fields
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'publication_year']
    # search fields
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']
    # ordering fields
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'author', 'publication_year']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        pub_year = serializer.validated_data.get('publication_year')
        if pub_year and pub_year > 2025:
            raise ValidationError("Publication year cannot be in the future.")
        super().perform_create(serializer)

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
   
