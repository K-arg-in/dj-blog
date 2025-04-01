from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    """Модельный менеджер, для того что бы упростить извлечение
    объектов из БД по полю статуса Опубликованые."""

    def get_queryset(self):
        """Получаем кверисет подмодели Статус модели Пост."""
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )


class Post(models.Model):
    """Модель поста с характеристиками:
    Название, слаг поста, тело поста(текст)."""
    class Status(models.TextChoices):
        """Модель статуса, отражающая является ли пост
        черновиком или опубликован."""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=256,)
    slug = models.SlugField(
        max_length=256,
        unique_for_date='pub_date'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now,)
    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    objects = models.Manager() # Менеджер применяемы по умолчанию
    published = PublishedManager() # Конкректно прикладной менеджер

    class Meta:
        ordering = ['-pub_date']
        # Определяет в модели индексы БД которые могут содержать
        # одно или несколько полей в возрастающем либо убывающем порядке,
        # или функциональные выражения и функции БД.
        indexes = [
            models.Index(fields=['-pub_date']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод отрисовывающий детальной отображение поста
        по параметрам:
          - год, месяц, день и слаг-поста."""
        return reverse(
            'blog:post_detail',
            args=[
                self.pub_date.year,
                self.pub_date.month,
                self.pub_date.day,
                self.slug
            ]
        )
