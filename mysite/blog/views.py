from django.http import Http404
from django.shortcuts import get_object_or_404, render


from .models import Post


def post_list(request):
    """Отображение информации о посте."""

    posts = Post.published.all() # Получаем все опубликованные объекты.
    context = {'posts': posts}
    # Закидываем в отображение резульатата реквест, шаблон и контекст
    return render(request, 'blog/post/list.html', context)

def post_detail(request, id):
    """Функция детального тображения одного опубликованного поста."""

    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED
    )
    context = {'post': post}
    return render(request, 'blog/post/detail.html', context)
