from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from .models import Post, Comment


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'description', 'text', 'date_pub', 'image']

        labels = {
            'title': 'Название',
            'description': 'Описание',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'описание'}),
            'date_pub': forms.DateTimeInput(),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 6:
            raise ValidationError('Заголовок слишком маленький!')
        else:
            return title

    def clean(self):
        return super().clean()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Текст комментария'
                })
        }