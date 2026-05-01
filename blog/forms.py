from django import forms
from .models import Post, Comment

# ── CHEATSHEET: ModelForm ─────────────────────────────────────────────────────
# ModelForm auto-generates HTML fields from a Model.
# Meta.fields controls which fields are shown in the form.
# Use fields = '__all__' to include every field (avoid in production for security).
# ─────────────────────────────────────────────────────────────────────────────

class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['title', 'content', 'author_name']  # explicitly whitelist fields


class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['name', 'comment_text']
