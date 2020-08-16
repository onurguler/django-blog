from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import RegistrationForm, PostCreateForm
from .models import Post


def index(request):
    posts = Post.objects.filter(published=True).order_by('-updated_at')
    return render(request, "index.html", context={"posts": posts})


def register(request):
    # users_count = User.objects.all().count()

    # if users_count != 0:
    #     return redirect('index')
    if request.user.is_authenticated:
        return redirect('index')

    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        form.save()

        username = form.cleaned_data["username"]
        password = form.cleaned_data['password1']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, "register.html", context={"form": form})


@login_required
def create_new_post(request):
    form = PostCreateForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.owner = request.user
        post.save()
        return redirect('index')

    return render(request, "create_post.html", context={"form": form})


def post_detail(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)

        if not post.published and post.owner != request.user:
            raise Http404()
    else:
        post = get_object_or_404(Post.objects.filter(
            published=True).all(), pk=post_id)
    return render(request, 'post_detail.html', context={'post': post})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(request.user.posts.all(), pk=post_id)
    form = PostCreateForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save()
        if post.published:
            return redirect('post_detail', post_id=post.pk)
        else:
            return redirect('list_drafts')
    return render(request, "edit_post.html", context={'form': form, 'post': post})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(request.user.posts.all(), pk=post_id)
    if request.POST:
        post.delete()
        return redirect('index')
    return render(request, 'post_delete_confirm.html', context={'post': post})


@login_required
def list_drafts(request):
    posts = request.user.posts.filter(published=False).order_by('-created_at')
    return render(request, 'list_drafts.html', context={'posts': posts})
