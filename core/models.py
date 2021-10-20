from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.utils import timezone


def user_avatar_path(instance, filename):
    return f'user_{instance.user.id}/avatar/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    about = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to=user_avatar_path)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username


def post_image_path(instance, filename):
    return f'user_{instance.author.id}/posts/{filename}'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    text = models.TextField(max_length=2500)
    date_pub = models.DateTimeField(default=timezone.now)
    date_edit = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='users_likes_it', blank=True)
    image = models.ImageField(upload_to=post_image_path)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return '#'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_pub = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author












# Create your models here.

# class Author(models.Model):
#     first_name = models.CharField(max_length=70)
#     last_name = models.CharField(max_length=70)

#     def __str__(self):
#         return self.first_name

# class Book(models.Model):
#     name = models.CharField(max_length=70)
#     text = models.TextField(max_length=500)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     page_amount = models.IntegerField()

#     def __str__(self):
#         return ' '.join(self.name, self.author)


