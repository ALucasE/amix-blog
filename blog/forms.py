from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='Nombre')
    email = forms.EmailField(label='Tu correo electronico')
    to = forms.EmailField(label='Correo electronico de destino')
    comments = forms.CharField(required=False, widget=forms.Textarea, label='Comentario')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField(label='Buscar')
