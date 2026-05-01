from django.db import models

# ── CHEATSHEET: ImageField ────────────────────────────────────────────────────
# ImageField  → stores a file path; requires Pillow; upload_to sets the sub-folder
# blank=True  → field is optional in forms
# null=True   → stores NULL in the database (use both together for optional files)
# ─────────────────────────────────────────────────────────────────────────────

class Product(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    # ImageField: requires Pillow installed; blank/null=True makes it optional
    image       = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    # ForeignKey: many Reviews for one Product; delete reviews when product deleted
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user_name  = models.CharField(max_length=100)
    rating     = models.IntegerField()   # 1–5; use validators in production
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} rated {self.product.name}: {self.rating}/5"
