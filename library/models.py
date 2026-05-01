from django.db import models

# ── CHEATSHEET: DateField vs DateTimeField ───────────────────────────────────
# DateField     → stores date only (YYYY-MM-DD)
# DateTimeField → stores date + time
# ─────────────────────────────────────────────────────────────────────────────

class Author(models.Model):
    name      = models.CharField(max_length=100)
    biography = models.TextField()
    birthdate = models.DateField()  # date only — no time component

    def __str__(self):
        return self.name


class Book(models.Model):
    title        = models.CharField(max_length=200)
    isbn         = models.CharField(max_length=20, unique=True)
    publish_date = models.DateField()
    summary      = models.TextField()
    # ForeignKey: many Books belong to one Author; books accessible via author.books.all()
    author       = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} by {self.author.name}"
