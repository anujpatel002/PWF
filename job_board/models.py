from django.db import models

# ── CHEATSHEET: DecimalField & URLField ──────────────────────────────────────
# DecimalField  → precise decimal numbers; always set max_digits & decimal_places
# URLField      → stores a URL string; validates format automatically
# ─────────────────────────────────────────────────────────────────────────────

class Company(models.Model):
    name     = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    industry = models.CharField(max_length=200)
    website  = models.URLField()  # validates URL format

    def __str__(self):
        return self.name


class JobPost(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    location    = models.CharField(max_length=200)
    salary      = models.DecimalField(max_digits=10, decimal_places=2)
    # ForeignKey: many JobPosts belong to one Company
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.company.name}"
