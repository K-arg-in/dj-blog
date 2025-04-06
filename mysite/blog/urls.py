from django.urls import path

from .views import post_comment, post_detail, post_list, post_share

app_name = 'blog'

urlpatterns = [
    # path('', PostListView.as_view(), name='post_list'),
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path(
        # Форматируем урлы, что бы каждый пост имел индидуальную ссылку
        # в виде параметров: год\месяц\день\слаг-поста
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        post_detail,
        name='post_detail'
    ),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
]
