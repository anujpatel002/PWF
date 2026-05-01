from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, CommentForm

# ── CHEATSHEET: Function-Based Views (FBV) CRUD ───────────────────────────────
# Pattern for every FBV:
#   GET  → show empty form / queryset
#   POST → validate form → save → redirect  (Post/Redirect/Get pattern)
# get_object_or_404 → returns 404 response if object not found (safe lookup)
# ─────────────────────────────────────────────────────────────────────────────


# LIST — query all objects, pass to template
def post_list(request):
    # order_by('-created_at') → newest first (- prefix = descending)
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


# CREATE — render blank form on GET, validate & save on POST
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # PRG: redirect after successful POST
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# DETAIL — fetch one object + handle related-model form (Comment) in same view
def post_detail(request, pk):
    post     = get_object_or_404(Post, pk=pk)  # 404 if not found
    comments = post.comments.all()             # reverse FK lookup via related_name

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment      = form.save(commit=False)  # don't write to DB yet
            comment.post = post                     # attach FK manually
            comment.save()                          # now write to DB
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post':     post,
        'comments': comments,
        'form':     form,
    })


# UPDATE — pre-populate form with existing instance
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # instance= tells Django to UPDATE
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)  # pre-fill form with current data

    return render(request, 'blog/post_form.html', {'form': form})


# DELETE — confirm on GET, delete on POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})
