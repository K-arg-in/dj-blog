from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render


from .models import Post


class PostListView(ListView):
    """Представление на основе класса ListView
    для отображения всех постов по параметрам."""

    queryset = Post.published.all()
    paginate_by = 3
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'


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
