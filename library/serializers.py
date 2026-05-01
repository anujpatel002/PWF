from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    # books_count: a computed read-only field using SerializerMethodField
    books_count = serializers.SerializerMethodField()

    class Meta:
        model  = Author
        fields = ['id', 'name', 'biography', 'birthdate', 'books_count']

    def get_books_count(self, obj):
        # obj is the Author instance; obj.books is the reverse FK manager
        return obj.books.count()


class BookSerializer(serializers.ModelSerializer):
    # Nested read-only: shows author name alongside the FK id
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model            = Book
        fields           = ['id', 'title', 'isbn', 'publish_date', 'summary',
                            'author', 'author_name']
        read_only_fields = ['author_name']
