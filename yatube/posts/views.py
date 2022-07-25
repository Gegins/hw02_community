from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    posts = Post.objects.all()[:10]
    context = {'title': title, 'posts': posts}
    return render(request, template, context)


def group_posts(request, slug):
    return 1
#    template = 'posts/group_list.html'
#    group = get_object_or_404(Group, slug=slug)
#    posts = group.posts.all()[:10]
#    title = f'Записи сообщества {group}'
#    context = {'title': title, 'group': group, 'posts': posts}
#    return render(request, template, context)
