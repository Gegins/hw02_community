from django.shortcuts import render, get_object_or_404


# Импортируем модель, чтобы обратиться к ней
from .models import Group, Post


def index(request):
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    posts = Post.objects.all()[:10]
    context = {
        'posts': posts,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    title = f'Записи сообщества {group}'
    posts = posts = group.posts.all()[:10]
    context = {'title': title, 'group': group, 'posts': posts}
    return render(request, template, context)
