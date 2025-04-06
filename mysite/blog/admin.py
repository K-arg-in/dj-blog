from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Регистрация модели поста в админ-панели."""

    # Отображает полей модели на странице Администрирования
    list_display = ['title', 'slug', 'author', 'pub_date', 'status']
    # Добавляет боковую панель фильтрации по полям
    list_filter = ['status', 'created', 'pub_date', 'author']
    # Добавляет строку поиска по названию, телу поста
    search_fields = ['title', 'body']
    # Автоматически генерирует слаг из нанзвания
    prepopulated_fields = {'slug': ('title',)}
    # Инкременирирует номер пользователя вместо строкового значения имени
    raw_id_fields = ['author']
    # Добавляет иерарзхию поисковых ответов в админке
    date_hierarchy = 'pub_date'
    ordering = ['status', 'pub_date']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Регистрация модели комментария в админ-панели."""

    # Отображает поля модели в админке
    list_display = ['name', 'post', 'email', 'created', 'active']
    # Отображает фильтрацию комментариев по параметрам (в боковой панели)
    list_filter = ['active', 'created', 'updated']
    # Поля по которым происходит поиск комментариев
    search_fields = ['name', 'email', 'body']
