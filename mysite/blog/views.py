from django.db.models import Count
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Post


#class PostListView(ListView):
#    """Представление на основе класса ListView
#    для отображения всех постов по параметрам."""
#
#    queryset = Post.published.all()
#    paginate_by = 3
#    context_object_name = 'posts'
#    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': posts,
            'tag': tag
        }
    )

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

    # Список активных комментариев в к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментирования пользователем
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids,
    ).exclude(id=post.id)
    similar_posts =similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-pub_date')[:4]

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
    }
    return render(request, 'blog/post/detail.html', context)

def post_share(request, post_id):
    """Функция позволяющая поделиться постом с другим человеком."""

    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # Форма была передана обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Валидация пройдена
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f'{cd['name']} Рекомендовано к прочтению.'
                f'{post.title}'
            )
            message = (
                f'Прочитать {post.title} на {post_url}\n\n'
                f'{cd['name']}\" комментарии: {cd['comments']}'
            )
            send_mail(
                subject,
                message,
                'filkargin@yandex.ru',
                [cd['to']],
                fail_silently=False,
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )

@require_POST
def post_comment(request, post_id):
    """Функция добавления комментария
    и рендеринга страницы коммента."""

    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в БД
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в БД
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )