from django.urls import path

from .views import post_detail, post_list

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path(
        # Форматируем урлы, что бы каждый пост имел индидуальную ссылку
        # в виде параметров: год\месяц\день\слаг-поста
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        post_detail,
        name='post_detail'
    ),
]
