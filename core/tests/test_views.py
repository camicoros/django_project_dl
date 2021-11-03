from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Post


class TestCoreViews(TestCase):
    def setUp(self) -> None:
        client = Client()
        self.response = client.get('/core/')
        return super().setUp()

    def test_index_view(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_content_index_view(self):
        self.assertContains(self.response, 'Main')


class TestLikePostView(TestCase):
    def setUp(self) -> None:
        my_user = User.objects.create(username='test', password='test', email='test@test.com')
        self.my_post = Post.objects.create(
            author=my_user,
            title='test',
            description='test',
            text='test',
        )
        return super().setUp()

    def test_login_redirect(self):
        self.client.login(username='test', password='test')
        
        request = self.client.get(reverse('like_post', args=(self.my_post.id,)))
        self.assertRedirects(request, '/core/feed/')


