from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    """Модель поста с характеристиками:
    Название, слаг поста, тело поста(текст)."""
    class Status(models.TextChoices):
        """Модель статуса, отражающая является ли пост
        черновиком или опубликован."""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=256,)
    slug = models.SlugField(max_length=256,)
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

    class Meta:
        ordering = ['-pub_date']
        indexes = [
            models.Index(fields=['-pub_date']),
        ]

    def __str__(self):
        return self.title
