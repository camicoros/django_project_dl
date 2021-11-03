from datetime import datetime
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import widgets
from .models import Profile, Post, Comment


admin.site.register(Profile)
admin.site.register(Comment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # fields = ['author', 'title', 'description', 'text', 'image', 'get_likes', ('date_pub', 'date_edit')]

    fieldsets = [
        ["Main parameters", {'fields': ['author', 'title']}],
        ["Detail info", {'fields': ['description', 'text']}],
    ]

    # exclude = ['author']
    readonly_fields = ['date_pub', 'date_edit', 'get_likes']

    list_display = ['__str__', 'author', 'title', 'get_likes']

    list_editable = ['author', 'title']

    list_filter = ['author', 'date_pub']

    search_fields = ['title', 'author__username']

    @staticmethod
    @admin.action(description='update date pub')
    def asdadadadassd(modeladmin, request, queryset):
        for post in queryset:
            post.title = 'ba'
            post.save()

    actions = ['asdadadadassd']



admin.site.unregister(User)


class ProfileInlineForm(forms.ModelForm):
    class Meta:
        model = Profile

        widgets = {
            'about': forms.Textarea(attrs={'rows': 4, 'cols': 10})
        }
        fields = '__all__'

class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['about', 'avatar', 'friends']
    filter_vertical = ['friends', ]
    form = ProfileInlineForm



class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(User)
class MyUserAdmin(UserAdmin):
    inlines = [ProfileInline, PostInline]