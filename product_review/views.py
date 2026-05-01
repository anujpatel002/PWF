from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Product, Review
from .forms import ProductForm, ReviewForm
from .serializers import ProductSerializer, ReviewSerializer


# ── HTML / FBV Views — full CRUD on Product + Review ─────────────────────────

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_review/product_list.html', {'products': products})


def product_detail(request, pk):
    """Show product detail; allow submitting a review inline (FK attach pattern)."""
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review         = form.save(commit=False)  # hold in memory, don't save yet
            review.product = product                   # attach FK
            review.save()                              # now persist to DB
            return redirect('product_review:product_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'product_review/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form':    form,
    })


def product_create(request):
    if request.method == 'POST':
        # request.FILES is required when the form has file/image uploads
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_review:product_list')
    else:
        form = ProductForm()
    return render(request, 'product_review/product_form.html', {'form': form})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_review:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_review/product_form.html', {'form': form})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()  # CASCADE deletes all related reviews automatically
        return redirect('product_review:product_list')
    return render(request, 'product_review/product_confirm_delete.html', {'product': product})


# ── DRF API Views ─────────────────────────────────────────────────────────────

class ProductListCreateView(generics.ListCreateAPIView):
    """GET /api/products/  →  list with nested reviews; POST  →  create product."""
    queryset         = Product.objects.prefetch_related('reviews').all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH /api/products/<pk>/  or  DELETE to remove a product."""
    queryset         = Product.objects.prefetch_related('reviews').all()
    serializer_class = ProductSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """GET /api/reviews/  →  list; POST  →  insert a new review."""
    queryset         = Review.objects.select_related('product').all()
    serializer_class = ReviewSerializer


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH /api/reviews/<pk>/  or  DELETE to remove a review."""
    queryset         = Review.objects.select_related('product').all()
    serializer_class = ReviewSerializer
