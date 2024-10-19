from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import CommentForm
from .forms import PostEditForm
from .forms import PostForm
from .models import Comment
from .models import Post
from .settings import INDEX_NPOSTS, MAX_DEPTH, BOARDS_PREFIXES


EMPTY_MESSAGE = "It is empty here!"


def index(request) -> HttpResponse:
    posts = Post.objects.order_by("-date").all()
    paginator = Paginator(posts, INDEX_NPOSTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "header": "news",
        "empty_message": EMPTY_MESSAGE,
    }
    return render(request, "app/index.html", context)


def papers(request) -> HttpResponse:
    posts = Post.objects.order_by("-date").filter(board="p")
    paginator = Paginator(posts, INDEX_NPOSTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "header": "papers",
        "empty_message": EMPTY_MESSAGE,
    }
    return render(request, "app/index.html", context)


def jobs(request) -> HttpResponse:
    posts = Post.objects.order_by("-date").filter(board="j")
    paginator = Paginator(posts, INDEX_NPOSTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "header": "jobs",
        "empty_message": EMPTY_MESSAGE,
    }
    return render(request, "app/index.html", context)


def code(request) -> HttpResponse:
    posts = Post.objects.order_by("-date").filter(board="c")
    paginator = Paginator(posts, INDEX_NPOSTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "header": "code",
        "empty_message": EMPTY_MESSAGE,
    }
    return render(request, "app/index.html", context)


def post_detail(request, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter(parent=None).order_by("-date")
    comment_form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "max_depth": MAX_DEPTH,
    }
    return render(request, "app/post_detail.html", context)


@login_required
def post_submit(request) -> HttpResponse:
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("app:index")
    else:
        form = PostForm()
    return render(request, "app/post_submit.html", {"form": form})


@login_required
def post_edit(request, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user:
        return redirect("app:post_detail", post_id=post_id)

    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return redirect("app:post_detail", post_id=post.id)
    else:
        form = PostEditForm()
    return render(request, "app/post_edit.html", {"form": form, "post": post})


@login_required
def post_delete(request, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user:
        return redirect("app:post_detail", post_id=post_id)

    if request.method == "GET":
        return render(request, "app/post_delete.html", {"post": post})
    post.delete()
    return redirect("app:index")


@login_required
@require_POST  # allows for embedding under post detail
def post_comment(request, post_id: int) -> HttpResponse:
    """Adds a top level comment to a post."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.parent = None
        comment.save()
    return redirect("app:post_detail", post_id=post_id)


def comment_detail(request, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, pk=comment_id)
    context = {
        "post": comment.post,
        "comments": [comment],
        "max_depth": MAX_DEPTH,
    }
    return render(request, "app/post_detail.html", context)


@login_required
def comment_reply(request, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = comment.post
            reply.user = request.user
            reply.parent = comment
            reply.save()
            return redirect("app:post_detail", post_id=reply.post.id)
    else:
        form = CommentForm()
    return render(request, "app/comment_reply.html", {"form": form, "comment": comment})


@login_required
def comment_delete(request, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user:
        return redirect("app:post_detail", post_id=comment.post.id)

    if request.method == "GET":
        return render(request, "app/comment_delete.html", {"comment": comment})
    elif request.method == "POST":
        comment.delete()
        return redirect("app:post_detail", post_id=comment.post.id)
    return redirect("app:post_detail", post_id=comment.post.id)


@login_required
def comment_edit(request, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user:
        return redirect("app:post_detail", post_id=comment.post.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment.save()
            return redirect("app:post_detail", post_id=comment.post.id)
    else:
        form = CommentForm()
    return render(request, "app/comment_edit.html", {"form": form, "comment": comment})

