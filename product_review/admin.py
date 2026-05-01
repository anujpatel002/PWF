from django.contrib import admin
from .models import Product, Review

# ── CHEATSHEET: Inline Admin ──────────────────────────────────────────────────
# TabularInline  → displays related objects in a compact table row format
# StackedInline  → displays related objects stacked vertically (more space)
# Use inlines inside a ModelAdmin to edit related objects on the same page.
# ─────────────────────────────────────────────────────────────────────────────

class ReviewInline(admin.TabularInline):
    """Embed reviews inside the Product admin page — edit related objects inline."""
    model   = Review
    extra   = 1          # number of blank extra rows shown for new entries
    fields  = ('user_name', 'rating', 'comment', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price')
    search_fields = ('name', 'description')
    list_filter   = ('price',)
    inlines       = [ReviewInline]   # ← shows reviews table inside Product admin


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('user_name', 'product', 'rating', 'created_at')
    list_filter   = ('rating', 'created_at')
    search_fields = ('user_name', 'comment')
    raw_id_fields = ('product',)
