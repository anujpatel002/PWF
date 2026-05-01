from django.urls import path
from . import views

# ── CHEATSHEET: URL Patterns ──────────────────────────────────────────────────
# path('<int:pk>/', ...)  → captures an integer from the URL as `pk`
# name='...'             → lets templates use {% url 'name' %} for reverse lookup
# ─────────────────────────────────────────────────────────────────────────────

app_name = 'blog'  # namespace: use {% url 'blog:post_list' %} in templates

urlpatterns = [
    path('',              views.post_list,   name='post_list'),    # GET  /blog/
    path('new/',          views.post_create, name='post_create'),  # GET/POST /blog/new/
    path('<int:pk>/',     views.post_detail, name='post_detail'),  # GET/POST /blog/<pk>/
    path('<int:pk>/edit/',   views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
]
