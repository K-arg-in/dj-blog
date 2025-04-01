from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render


from .models import Post


def post_list(request):
    """Отображение информации о посте."""

    post_list = Post.published.all() # Получаем все опубликованные объекты.
    paginator = Paginator(post_list, 3) # Пагинатор отражающий по 3 поста на странице
    page_number = request.GET.get('page', 1) # Извлекаем параметр страницы page
    posts = paginator.page(page_number) # Получаем объекты желаемой страницы
    context = {'posts': posts}
    # Закидываем в отображение резульатата реквест, шаблон и контекст
    return render(request, 'blog/post/list.html', context)

def post_detail(request, year, month, day, post):
    """Функция детального тображения одного опубликованного поста."""

    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        # реализуем логику отображения в представлении по параметрам
        # год, меся, день, слаг-поста
        slug=post,
        pub_date__year=year,
        pub_date__month=month,
        pub_date__day=day
    )
    context = {'post': post}
    return render(request, 'blog/post/detail.html', context)
