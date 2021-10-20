from django.conf.urls import url
from django.urls.conf import path
from django.views.generic import TemplateView

from .views import (
    PostDetailView, 
    LikePostView, IndexView, FeedView, PostCreateView, PostDelete, EditView
)
from .urls_auth import urlpatterns as auth_patterns

app_name = 'core'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^posts/(?P<post_id>[0-9]+)/$', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/edit/', EditView.as_view(), name='post_edit'),
    path('posts/<int:post_id>/delete/', PostDelete.as_view(), name='post_delete'),
    path('posts/<int:post_id>/delete-success/', TemplateView.as_view(template_name='core/delete_success.html'), name='post_delete_success'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('feed/', FeedView.as_view(), name='feed')
]

urlpatterns += auth_patterns