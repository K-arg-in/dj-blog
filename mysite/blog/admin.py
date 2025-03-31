from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Отображает поля модели на странице Администрирования
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
