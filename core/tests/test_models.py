from datetime import datetime, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from core.models import Post, Profile


class TestPostModel(TestCase):

    def test_date_edit(self):
        with self.assertRaises(ValidationError):
            my_user = User.objects.create(username='test', password='test', email='test@test.com')
            my_post = Post.objects.create(
                author=my_user,
                title='test',
                description='test',
                text='test',
            )
            my_post.date_edit = datetime.now() + timedelta(days=1)
            my_post.full_clean()
            my_post.save()


class TestProfileModel(TestCase):
    def test_create_profile_with_user(self):
        my_user = User.objects.create(username='test', password='test', email='test@test.com')
        self.assertIsNotNone(my_user.profile)
