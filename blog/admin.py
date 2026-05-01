from django.contrib import admin
from .models import Post, Comment

# ── CHEATSHEET: Django Admin Registration ────────────────────────────────────
# admin.site.register(Model)          → basic registration (all fields visible)
# @admin.register(Model)              → decorator shortcut for ModelAdmin class
# list_display  → columns shown in the changelist table
# list_filter   → sidebar filter options
# search_fields → fields Django searches when using the search box
# raw_id_fields → replaces FK dropdown with a lookup popup (good for large tables)
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author_name', 'created_at', 'updated_at')
    list_filter   = ('author_name', 'created_at')
    search_fields = ('title', 'content', 'author_name')
    ordering      = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('name', 'post', 'created_at')
    list_filter   = ('created_at',)
    search_fields = ('name', 'comment_text')
    raw_id_fields = ('post',)  # avoids loading all posts in a dropdown
