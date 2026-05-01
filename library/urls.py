from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # ── HTML Views ────────────────────────────────────────────────────────────
    path('authors/add/',              views.add_author,   name='add_author'),
    path('authors/',                  views.author_list,  name='author_list'),
    path('authors/<int:author_id>/',  views.author_books, name='author_books'),

    # ── REST API Endpoints ────────────────────────────────────────────────────
    path('api/authors/',           views.AuthorListCreateView.as_view(),          name='author_api_list_create'),
    path('api/authors/<int:pk>/',  views.AuthorRetrieveUpdateDestroyView.as_view(), name='author_api_detail'),
    path('api/books/',             views.BookListCreateView.as_view(),             name='book_list_create'),
    path('api/books/<int:pk>/',    views.BookRetrieveUpdateDestroyView.as_view(),  name='book_detail'),
]
