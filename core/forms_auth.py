
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, UsernameField
)
from django.contrib.auth.models import User
from django.db import models
from django.forms import fields
from django.utils.translation import gettext_lazy as _
from .models import Profile


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'authfocus': True,
        'placeholder': 'Логин',
        'class': 'form-control'
    }))
    
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
        'class': 'form-control'
    }),
    strip=False,
    )

    error_messages = {
        'invalid_login': 'Введён неправильный логин или пароль'
    }


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'class': 'form-control'
        }),
    )

    password2 = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Подтвердите пароль',
            'class': 'form-control'
        }),
        help_text=_("Enter the same password as above")
    )

    error_messages = {
        'password_mismatch': 'Пароли не совпадают'
    }

    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
            'authfocus': True,
            'placeholder': 'Логин',
            'class': 'form-control'
        }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # username = self.cleaned_data.get('username')

        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('email должен быть уникальным')
        return email


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'avatar']
        labels = {
            'about': "Обо мне",
            'avatar': "Фото"
        }