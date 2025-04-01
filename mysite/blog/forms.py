from django import forms


class EmailPostForm(forms.Form):
    """Форма для заполнения имени, 
    емейла, адреса отправки и комментариев."""\

    name = forms.CharField(max_length=25,)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        # изменяем виджет явным образом
        widget=forms.Textarea
    )
