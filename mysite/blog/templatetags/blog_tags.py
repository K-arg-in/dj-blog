from django import template
from django.db.models import Count
from ..models import Post

register = template.Library() # регистратор шаблонных тегов и фильтров приложения

@register.simple_tag
def total_posts():
    """Простой шаблонный тег, который возвращает количество 
    постов опубликованных в блоге."""
    return Post.published.count()

@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    """Шаблонный тег который отображает 5 последних
    опубликованных постов под тегом который считает кол-во постов."""
    latest_posts = Post.published.order_by("-pub_date")[:count]
    return {"latest_posts": latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    """Шаблонный тег который агрегирует все комментарии
    к каждому отдельно взятому посту."""
    return Post.published.annotate(
        total_comments=Count("comments")
    ).order_by("-total_comments")[:count]
