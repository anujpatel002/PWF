# PWF — Python/Django Pattern Workshop Files

A **cheat sheet and pattern library** for fast Django development.  
Every app is a working mini-project demonstrating the patterns described in [CHEATSHEET.md](CHEATSHEET.md).

---

## What's Inside

| App | Demonstrates |
|-----|-------------|
| `blog/` | Full FBV CRUD · ForeignKey · ModelForm · `commit=False` |
| `course_enrollment/` | ManyToManyField · M2M add/remove · Django Admin M2M widget |
| `job_board/` | DRF API CRUD · ForeignKey · Nested serializer · Admin inline |
| `library/` | DRF API CRUD · ForeignKey · `SerializerMethodField` · CBV |
| `product_review/` | Image upload · Full FBV + API CRUD · TabularInline Admin |

---

## Quick Start

```bash
# 1. Install dependencies
pip install django djangorestframework pillow

# 2. Add apps and REST framework to settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'blog',
    'course_enrollment',
    'job_board',
    'library',
    'product_review',
]

# 3. Wire URLs in myproject/urls.py
from django.urls import path, include
urlpatterns = [
    path('admin/',    admin.site.urls),
    path('blog/',     include('blog.urls',              namespace='blog')),
    path('courses/',  include('course_enrollment.urls', namespace='course_enrollment')),
    path('jobs/',     include('job_board.urls',         namespace='job_board')),
    path('library/',  include('library.urls',           namespace='library')),
    path('shop/',     include('product_review.urls',    namespace='product_review')),
]

# 4. Run migrations and start
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # access /admin/
python manage.py runserver
```

---

## Navigation

```
repo/
├── CHEATSHEET.md              ← Main reference (start here)
│
├── blog/                      ← FBV CRUD + ForeignKey
│   ├── models.py              Fields, FK, __str__
│   ├── forms.py               ModelForm, Meta.fields
│   ├── views.py               list/create/detail/update/delete
│   ├── urls.py                path(), app_name namespace
│   └── admin.py               @admin.register, list_display
│
├── course_enrollment/         ← ManyToMany
│   ├── models.py              ManyToManyField
│   ├── views.py               .add(), .all() on M2M
│   ├── forms.py               ModelForm
│   ├── urls.py
│   └── admin.py               filter_horizontal for M2M
│
├── job_board/                 ← DRF API (Company + JobPost)
│   ├── models.py              FK, DecimalField, URLField
│   ├── serializers.py         ModelSerializer, nested field
│   ├── views.py               ListCreateAPIView, RetrieveUpdateDestroyAPIView
│   ├── forms.py
│   ├── urls.py                API + HTML URLs mixed
│   └── admin.py               raw_id_fields
│
├── library/                   ← DRF API (Author + Book)
│   ├── models.py              FK, DateField
│   ├── serializers.py         SerializerMethodField, nested read-only
│   ├── views.py               CBV API views
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── product_review/            ← Full CRUD + ImageField + Inline Admin
│   ├── models.py              ImageField, blank/null
│   ├── serializers.py         Nested serializer, computed avg_rating
│   ├── views.py               request.FILES, full FBV + API CRUD
│   ├── forms.py
│   ├── urls.py
│   └── admin.py               TabularInline (ReviewInline inside ProductAdmin)
│
└── templates/
    ├── blog/
    ├── course_enrollment/
    ├── jobs/
    ├── library/
    └── product_review/
```

---

## Key Concepts Covered

- ✅ **Models**: CharField, TextField, IntegerField, DecimalField, ImageField, URLField, DateField, DateTimeField, EmailField
- ✅ **Relationships**: ForeignKey (many-to-one), ManyToManyField
- ✅ **Forms**: ModelForm, `commit=False` pattern, file upload with `request.FILES`
- ✅ **Views FBV**: list, create, detail, update, delete (full CRUD)
- ✅ **Views CBV (DRF)**: ListCreateAPIView, RetrieveUpdateDestroyAPIView
- ✅ **Serializers**: ModelSerializer, `SerializerMethodField`, nested serializer, `read_only_fields`
- ✅ **API**: Insert (POST) and Delete (DELETE) via DRF on job_board, library, product_review
- ✅ **Admin**: `@admin.register`, `list_display`, `list_filter`, `search_fields`, `raw_id_fields`, `filter_horizontal`, `TabularInline`

→ **[Open CHEATSHEET.md](CHEATSHEET.md)** for copy-paste snippets of every pattern above.
