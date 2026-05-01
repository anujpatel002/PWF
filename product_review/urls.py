from django.urls import path
from . import views

app_name = 'product_review'

urlpatterns = [
    # ── HTML Views ────────────────────────────────────────────────────────────
    path('products/',              views.product_list,   name='product_list'),
    path('products/new/',          views.product_create, name='product_create'),
    path('products/<int:pk>/',     views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/',   views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # ── REST API Endpoints ────────────────────────────────────────────────────
    path('api/products/',           views.ProductListCreateView.as_view(),           name='product_api_list_create'),
    path('api/products/<int:pk>/',  views.ProductRetrieveUpdateDestroyView.as_view(), name='product_api_detail'),
    path('api/reviews/',            views.ReviewListCreateView.as_view(),             name='review_api_list_create'),
    path('api/reviews/<int:pk>/',   views.ReviewRetrieveUpdateDestroyView.as_view(),  name='review_api_detail'),
]
