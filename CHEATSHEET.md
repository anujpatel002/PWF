# 🐍 Django Cheat Sheet — Fast Development Reference

> **Ctrl+F** to jump to any section. Every snippet is drawn from the working code in this repo.

---

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Models — Fields & Relationships](#2-models--fields--relationships)
3. [Migrations](#3-migrations)
4. [Forms — HTML & Django ModelForm](#4-forms--html--django-modelform)
5. [Views — Function-Based (FBV) CRUD](#5-views--function-based-fbv-crud)
6. [Views — Class-Based (CBV) with DRF API](#6-views--class-based-cbv-with-drf-api)
7. [Serializers (DRF)](#7-serializers-drf)
8. [URL Configuration](#8-url-configuration)
9. [Django Admin Panel](#9-django-admin-panel)
10. [Templates — Snippets](#10-templates--snippets)
11. [Common Patterns Quick Reference](#11-common-patterns-quick-reference)
12. [API Endpoints — Insert / Delete via DRF](#12-api-endpoints--insert--delete-via-drf)

---

## 1. Project Setup

```bash
# Install
pip install django djangorestframework pillow

# New project & app
django-admin startproject myproject
cd myproject
python manage.py startapp myapp

# Register app in settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'myapp',
]

# Run dev server
python manage.py runserver
```

---

## 2. Models — Fields & Relationships

### Field Type Quick Reference

| Field | Use For | Key Options |
|-------|---------|-------------|
| `CharField` | Short text | `max_length` required |
| `TextField` | Long/unlimited text | — |
| `IntegerField` | Whole numbers | — |
| `DecimalField` | Precise decimals (money) | `max_digits`, `decimal_places` |
| `FloatField` | Approximate decimals | — |
| `BooleanField` | True/False | `default=False` |
| `DateField` | Date only | `auto_now_add`, `auto_now` |
| `DateTimeField` | Date + time | `auto_now_add`, `auto_now` |
| `EmailField` | Email address (validated) | — |
| `URLField` | URL string (validated) | — |
| `ImageField` | File path (requires Pillow) | `upload_to`, `blank=True`, `null=True` |
| `SlugField` | URL-friendly string | `max_length` |

### auto_now_add vs auto_now

```python
created_at = models.DateTimeField(auto_now_add=True)  # set ONCE on creation
updated_at = models.DateTimeField(auto_now=True)       # updated on EVERY save
```

### ForeignKey (Many-to-One)

```python
# blog/models.py
class Post(models.Model):
    title   = models.CharField(max_length=200)
    content = models.TextField()

class Comment(models.Model):
    # Many comments → one post
    # on_delete=CASCADE: deleting a Post deletes all its Comments
    # related_name='comments' → post.comments.all()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
```

**on_delete options:**

| Option | Behaviour |
|--------|-----------|
| `CASCADE` | Delete child rows when parent is deleted |
| `PROTECT` | Prevent parent deletion if children exist |
| `SET_NULL` | Set FK to NULL (requires `null=True`) |
| `SET_DEFAULT` | Set FK to a default value |
| `DO_NOTHING` | Do nothing (may break integrity) |

### ManyToManyField

```python
# course_enrollment/models.py
class Course(models.Model):
    name = models.CharField(max_length=100)

class Student(models.Model):
    name    = models.CharField(max_length=100)
    # Django auto-creates the junction table
    # related_name='students' → course.students.all()
    courses = models.ManyToManyField(Course, related_name='students', blank=True)

# Usage
student.courses.add(course)      # enrol
student.courses.remove(course)   # un-enrol
student.courses.all()            # list courses for a student
course.students.all()            # list students on a course (reverse M2M)
```

### `__str__` pattern

```python
def __str__(self):
    return self.title                          # simple field
    return f"Comment by {self.name}"           # f-string
    return f"{self.title} @ {self.company.name}"  # traverse FK
```

### Optional / Nullable fields

```python
image = models.ImageField(upload_to='products/', blank=True, null=True)
# blank=True → field is optional in forms
# null=True  → stores NULL in the database
# Use both together for optional fields
```

---

## 3. Migrations

```bash
python manage.py makemigrations   # generate migration files from model changes
python manage.py migrate          # apply migrations to the database
python manage.py showmigrations   # list all migrations and their status
python manage.py sqlmigrate app 0001  # show raw SQL for a migration
```

---

## 4. Forms — HTML & Django ModelForm

### ModelForm (recommended)

```python
# blog/forms.py
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['title', 'content', 'author_name']  # whitelist fields
        # OR: fields = '__all__'  — include every field (avoid in production)

class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['name', 'comment_text']
```

### Render form in template

```html
<!-- Three rendering options: -->
{{ form.as_p }}       <!-- each field wrapped in <p> tags -->
{{ form.as_table }}   <!-- each field in a <tr> -->
{{ form.as_ul }}      <!-- each field in a <li> -->

<!-- Full form block -->
<form method="POST">
  {% csrf_token %}   <!-- always required for POST forms -->
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>

<!-- File/image upload: add enctype -->
<form method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Upload</button>
</form>
```

### commit=False — attach FK before saving

```python
# Scenario: save a Comment but first attach it to a Post
if form.is_valid():
    comment      = form.save(commit=False)  # create instance without DB write
    comment.post = post                     # manually set the FK
    comment.save()                          # now write to DB
```

---

## 5. Views — Function-Based (FBV) CRUD

### Full CRUD Template

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

# LIST
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # - = descending
    return render(request, 'blog/post_list.html', {'posts': posts})

# CREATE
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:post_list')  # PRG: redirect after POST
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

# DETAIL
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # returns 404 if not found
    return render(request, 'blog/post_detail.html', {'post': post})

# UPDATE
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # instance= → UPDATE mode
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)  # pre-fill with existing data
    return render(request, 'blog/post_form.html', {'form': form})

# DELETE
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
```

### File upload in view

```python
# Pass request.FILES when the form contains file/image fields
form = ProductForm(request.POST, request.FILES)
```

### Filter via query string

```python
# URL: /jobs/?company=3
company_id = request.GET.get('company')   # read ?company=X from URL
if company_id:
    jobs = jobs.filter(company_id=company_id)
```

---

## 6. Views — Class-Based (CBV) with DRF API

### Generic API Views

```python
from rest_framework import generics
from .models import JobPost
from .serializers import JobPostSerializer

# LIST + CREATE  →  GET /api/jobs/  and  POST /api/jobs/
class JobPostListCreateView(generics.ListCreateAPIView):
    queryset         = JobPost.objects.all()
    serializer_class = JobPostSerializer

# RETRIEVE + UPDATE + DELETE  →  GET/PUT/PATCH/DELETE /api/jobs/<pk>/
class JobPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset         = JobPost.objects.all()
    serializer_class = JobPostSerializer
```

### Generic View Cheatsheet

| Class | HTTP Methods | Purpose |
|-------|-------------|---------|
| `ListAPIView` | GET | List only |
| `CreateAPIView` | POST | Create only |
| `ListCreateAPIView` | GET + POST | List + Create |
| `RetrieveAPIView` | GET | Detail only |
| `UpdateAPIView` | PUT, PATCH | Update only |
| `DestroyAPIView` | DELETE | Delete only |
| `RetrieveUpdateAPIView` | GET + PUT/PATCH | Detail + Update |
| `RetrieveUpdateDestroyAPIView` | GET + PUT/PATCH + DELETE | Full detail CRUD |

### Performance: select_related & prefetch_related

```python
# select_related  → SQL JOIN; use for ForeignKey / OneToOne (single object)
JobPost.objects.select_related('company').all()

# prefetch_related → separate query then Python join; use for ManyToMany / reverse FK
Product.objects.prefetch_related('reviews').all()
```

---

## 7. Serializers (DRF)

### Basic ModelSerializer

```python
from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Company
        fields = '__all__'                    # all fields
        # fields = ['id', 'name', 'location'] # or whitelist
        # read_only_fields = ['created_at']   # shown but not accepted in POST
```

### Nested / Computed fields

```python
class JobPostSerializer(serializers.ModelSerializer):
    # Read-only field from a related object (traverse FK with dot notation)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model  = JobPost
        fields = ['id', 'title', 'company', 'company_name', 'salary']

class AuthorSerializer(serializers.ModelSerializer):
    # Computed field using a method
    books_count = serializers.SerializerMethodField()

    class Meta:
        model  = Author
        fields = ['id', 'name', 'books_count']

    def get_books_count(self, obj):   # method name: get_<field_name>
        return obj.books.count()

class ProductSerializer(serializers.ModelSerializer):
    # Nested serializer: embed related objects in the response
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model  = Product
        fields = ['id', 'name', 'price', 'reviews']
```

---

## 8. URL Configuration

### App-level urls.py

```python
# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'   # namespace: {% url 'blog:post_list' %} in templates

urlpatterns = [
    path('',              views.post_list,   name='post_list'),
    path('new/',          views.post_create, name='post_create'),
    path('<int:pk>/',     views.post_detail, name='post_detail'),
    path('<int:pk>/edit/',   views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    # API endpoints
    path('api/posts/',          views.PostListCreateView.as_view(),           name='post_api_list'),
    path('api/posts/<int:pk>/', views.PostRetrieveUpdateDestroyView.as_view(), name='post_api_detail'),
]
```

### Project-level urls.py

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',        admin.site.urls),
    path('blog/',         include('blog.urls',              namespace='blog')),
    path('courses/',      include('course_enrollment.urls', namespace='course_enrollment')),
    path('jobs/',         include('job_board.urls',         namespace='job_board')),
    path('library/',      include('library.urls',           namespace='library')),
    path('shop/',         include('product_review.urls',    namespace='product_review')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # serve uploaded files in dev
```

### URL Path Converters

| Converter | Example | Matches |
|-----------|---------|---------|
| `<int:pk>` | `/post/5/` | Positive integer |
| `<str:slug>` | `/post/hello-world/` | Any non-empty string |
| `<slug:slug>` | `/post/hello-world/` | Letters, numbers, hyphens |
| `<uuid:id>` | `/post/550e8400.../` | UUID |

---

## 9. Django Admin Panel

### Register a model

```python
# Simple registration
admin.site.register(Post)

# With ModelAdmin (recommended)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author_name', 'created_at')  # table columns
    list_filter   = ('author_name', 'created_at')           # sidebar filters
    search_fields = ('title', 'content')                    # search box fields
    ordering      = ('-created_at',)                        # default sort
    raw_id_fields = ('author',)                             # FK lookup popup
```

### Inline Admin (edit related objects on parent page)

```python
# product_review/admin.py
class ReviewInline(admin.TabularInline):   # or StackedInline for vertical layout
    model  = Review
    extra  = 1                             # number of blank extra rows
    fields = ('user_name', 'rating', 'comment')
    readonly_fields = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]               # reviews table embedded in Product admin
```

### ManyToMany widget

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    filter_horizontal = ('courses',)  # dual-list widget for M2M field
    # OR: filter_vertical = ('courses',)
```

### Admin customisation options

```python
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display       = ('field1', 'field2')   # columns in list view
    list_filter        = ('field1',)            # sidebar filter
    search_fields      = ('field1', 'field2')   # fields searched by search box
    ordering           = ('-created_at',)       # default ordering
    raw_id_fields      = ('fk_field',)          # popup for FK (large tables)
    filter_horizontal  = ('m2m_field',)         # dual-list widget for M2M
    readonly_fields    = ('created_at',)        # shown but not editable
    list_per_page      = 25                     # pagination
    date_hierarchy     = 'created_at'           # date drill-down navigation
```

### Create superuser

```bash
python manage.py createsuperuser
# Then visit http://127.0.0.1:8000/admin/
```

---

## 10. Templates — Snippets

### Loop over a queryset

```html
{% for post in posts %}
  <h2>{{ post.title }}</h2>
  <p>{{ post.author_name }} | {{ post.created_at|date:"Y-m-d" }}</p>
{% empty %}
  <p>No posts found.</p>   <!-- shown when queryset is empty -->
{% endfor %}
```

### Reverse URL with namespace

```html
<a href="{% url 'blog:post_list' %}">All Posts</a>
<a href="{% url 'blog:post_detail' post.pk %}">{{ post.title }}</a>
<a href="{% url 'blog:post_update' post.pk %}">Edit</a>
```

### Conditionals

```html
{% if user.is_authenticated %}
  <a href="{% url 'blog:post_create' %}">New Post</a>
{% endif %}

{% if product.image %}
  <img src="{{ product.image.url }}" alt="{{ product.name }}">
{% endif %}
```

### Template inheritance

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<body>
  {% block content %}{% endblock %}
</body>
</html>

<!-- child template -->
{% extends 'base.html' %}
{% block content %}
  <h1>My Page</h1>
{% endblock %}
```

### Common template filters

```html
{{ post.created_at|date:"Y-m-d" }}     <!-- format date -->
{{ post.content|truncatewords:30 }}     <!-- truncate to 30 words -->
{{ post.content|linebreaks }}           <!-- \n → <br> / <p> -->
{{ name|lower }}                        <!-- lowercase -->
{{ name|upper }}                        <!-- uppercase -->
{{ price|floatformat:2 }}              <!-- 2 decimal places -->
```

---

## 11. Common Patterns Quick Reference

### QuerySet Operations

```python
# Retrieve
Post.objects.all()                          # all records
Post.objects.get(pk=1)                      # single record (raises error if missing)
Post.objects.filter(author_name='Alice')    # WHERE clause
Post.objects.exclude(rating__lt=3)         # NOT WHERE
Post.objects.order_by('-created_at')       # ORDER BY (- = DESC)
Post.objects.filter(...).order_by(...)     # chain calls
Post.objects.first() / .last()             # first / last record
Post.objects.count()                       # COUNT(*)

# Field lookups
Post.objects.filter(title__contains='Django')   # LIKE '%Django%'
Post.objects.filter(title__icontains='django')  # case-insensitive
Post.objects.filter(rating__gte=4)              # >=
Post.objects.filter(rating__in=[4, 5])          # IN (4,5)
Post.objects.filter(created_at__year=2024)      # date part

# Performance
Post.objects.select_related('author')           # JOIN for FK
Post.objects.prefetch_related('comments')       # separate query for reverse FK / M2M

# Create / Update / Delete
post = Post.objects.create(title='Hello', content='...')  # INSERT in one line
Post.objects.filter(author_name='Bob').update(author_name='Robert')  # bulk UPDATE
Post.objects.filter(created_at__year=2020).delete()                  # bulk DELETE
```

### get_object_or_404

```python
# Returns 404 HTTP response if object not found — always prefer over .get()
from django.shortcuts import get_object_or_404
post = get_object_or_404(Post, pk=pk)
post = get_object_or_404(Post, slug=slug, published=True)  # multiple conditions
```

### Post/Redirect/Get (PRG) Pattern

```python
# Prevents duplicate form submission on browser refresh
if form.is_valid():
    form.save()
    return redirect('blog:post_list')   # redirect to list after successful POST
```

### ManyToMany operations

```python
student.courses.add(course)              # add one
student.courses.add(course1, course2)    # add multiple
student.courses.remove(course)           # remove one
student.courses.set([course1, course2])  # replace all
student.courses.clear()                  # remove all
student.courses.all()                    # list all related

# Check membership
course in student.courses.all()
student.courses.filter(pk=course.pk).exists()
```

---

## 12. API Endpoints — Insert / Delete via DRF

All API views in this repo use `ListCreateAPIView` (GET + POST) and
`RetrieveUpdateDestroyAPIView` (GET + PUT/PATCH + **DELETE**).

### Job Board API

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/companies/` | List all companies |
| POST | `/api/companies/` | **Insert** a company |
| GET | `/api/companies/<pk>/` | Get company detail |
| PUT/PATCH | `/api/companies/<pk>/` | Update company |
| DELETE | `/api/companies/<pk>/` | **Delete** company |
| GET | `/api/jobs/` | List all jobs |
| POST | `/api/jobs/` | **Insert** a job post |
| DELETE | `/api/jobs/<pk>/` | **Delete** a job post |

### Library API

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/authors/` | List all authors |
| POST | `/api/authors/` | **Insert** an author |
| DELETE | `/api/authors/<pk>/` | **Delete** an author + all books (CASCADE) |
| GET | `/api/books/` | List all books |
| POST | `/api/books/` | **Insert** a book |
| DELETE | `/api/books/<pk>/` | **Delete** a book |

### Product Review API

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/products/` | List products with nested reviews |
| POST | `/api/products/` | **Insert** a product |
| DELETE | `/api/products/<pk>/` | **Delete** product + all reviews (CASCADE) |
| GET | `/api/reviews/` | List all reviews |
| POST | `/api/reviews/` | **Insert** a review |
| DELETE | `/api/reviews/<pk>/` | **Delete** a review |

### Example: curl / httpie

```bash
# Insert a company
curl -X POST http://127.0.0.1:8000/api/companies/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme","location":"NY","industry":"Tech","website":"https://acme.com"}'

# Delete a job post
curl -X DELETE http://127.0.0.1:8000/api/jobs/5/

# Insert a book
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Django for Beginners","isbn":"123456","publish_date":"2023-01-01","summary":"...","author":1}'
```

---

## App Map

| App | Models | Relations | Has API |
|-----|--------|-----------|---------|
| `blog` | Post, Comment | FK (Comment→Post) | — |
| `course_enrollment` | Course, Student | M2M (Student↔Course) | — |
| `job_board` | Company, JobPost | FK (JobPost→Company) | ✅ Full CRUD |
| `library` | Author, Book | FK (Book→Author) | ✅ Full CRUD |
| `product_review` | Product, Review | FK (Review→Product) | ✅ Full CRUD |

---

*See each app's `models.py`, `views.py`, `forms.py`, `serializers.py`, `admin.py`, and `urls.py` for fully annotated working code.*
