from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import PostForm


# Импортируем модель, чтобы обратиться к ней
from .models import Group, Post, User


@login_required
def index(request):
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    title = f'Записи сообщества {group}'
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'title': title, 'group': group, 'page_obj': page_obj}
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    title = f'Профайл пользователя {author.get_full_name()}'
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'title': title, 'username': author.get_full_name(),
        'count_posts': paginator.count, 'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = Post.objects.get(pk=post_id)
    title = post.text[:30]
    count_posts = len(Post.objects.filter(author=post.author))
    context = {
        'title': title, 'post': post, 'count_posts': count_posts}
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    action = 'posts:post_create'
    title = 'Новый пост'
    confirm = 'Создать новый пост'
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author.username)
    else:
        form = PostForm()
    context = {
        'confirm': confirm, 'title': title, 'form': form, 'action': action}
    return render(request, template, context)


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        template = 'posts/create_post.html'
        # action = 'posts:post_edit'
        # text = post.text
        title = 'Редактировать пост'
        confirm = 'Сохранить изменения'
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('posts:profile', username=post.author.username)
        else:
            form = PostForm(instance=post)
            context = {
                'confirm': confirm, 'title': title, 'is_edit': True,
                'form': form, 'post': post}
            return render(request, template, context)
    else:
        return redirect('posts:post_detail', post_id)
