from django import forms

from .models import Comment

class EmailPostForm(forms.Form):
    """Форма для заполнения имени, 
    емейла, адреса отправки и комментариев."""

    name = forms.CharField(max_length=25,)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        # изменяем виджет явным образом
        widget=forms.Textarea
    )


class CommentForm(forms.Form):
    """Форма реализующая отображения комментария
    с полями:
    названия, текста, почты."""

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']