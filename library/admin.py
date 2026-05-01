from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display  = ('name', 'birthdate')
    search_fields = ('name', 'biography')
    ordering      = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'isbn', 'publish_date')
    list_filter   = ('author', 'publish_date')
    search_fields = ('title', 'isbn')
    raw_id_fields = ('author',)
    ordering      = ('title',)
