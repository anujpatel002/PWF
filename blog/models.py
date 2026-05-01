from django.db import models

# ── CHEATSHEET: Model Field Types ────────────────────────────────────────────
# CharField       → short text with max_length required
# TextField       → unlimited text (no max_length)
# DateTimeField   → date + time; auto_now_add=True sets once on create,
#                   auto_now=True updates on every save
# ForeignKey      → many-to-one relationship; on_delete controls cascade behaviour
#                   related_name lets you do parent.children.all()
# ─────────────────────────────────────────────────────────────────────────────

class Post(models.Model):
    title       = models.CharField(max_length=200)
    content     = models.TextField()
    author_name = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True)  # set once at creation
    updated_at  = models.DateTimeField(auto_now=True)      # updated on every save

    def __str__(self):
        # __str__ is shown in admin list and shell repr
        return self.title


class Comment(models.Model):
    # ForeignKey = many-to-one: many Comments belong to one Post
    # related_name='comments' → post.comments.all()
    post         = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name         = models.CharField(max_length=100)
    comment_text = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on '{self.post.title}'"
