from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from .models import Book, Author
from .forms import AuthorForm
from .serializers import AuthorSerializer, BookSerializer


# ── HTML / FBV Views ─────────────────────────────────────────────────────────

def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:author_list')
    else:
        form = AuthorForm()
    return render(request, 'library/add_author.html', {'form': form})


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})


def author_books(request, author_id):
    """Retrieve all books written by one author (reverse FK via related_name)."""
    author = get_object_or_404(Author, pk=author_id)
    books  = author.books.all()  # related_name='books' → author.books manager
    return render(request, 'library/author_books.html', {
        'author': author,
        'books':  books,
    })


# ── DRF API Views ─────────────────────────────────────────────────────────────

class AuthorListCreateView(generics.ListCreateAPIView):
    """GET /api/authors/  →  list; POST  →  create."""
    queryset         = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """GET /api/authors/<pk>/  →  detail; PUT/PATCH  →  update; DELETE  →  remove."""
    queryset         = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """GET /api/books/  →  list; POST  →  insert new book."""
    queryset         = Book.objects.select_related('author').all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """GET /api/books/<pk>/  →  detail; PUT/PATCH  →  update; DELETE  →  remove book."""
    queryset         = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
