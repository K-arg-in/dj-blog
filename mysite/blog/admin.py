from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Отображает поля модели на странице Администрирования
    list_display = ['title', 'slug', 'author', 'pub_date', 'status']
    list_filter = ['status', 'created', 'pub_date', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'pub_date'
    ordering = ['status', 'pub_date']
