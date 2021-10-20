from django.db import models
from django.db.models.aggregates import Count
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View

from .models import Comment, Post
from .forms import CommentForm, PostForm


class IndexView(ListView):
    model = Post
    template_name = 'core/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return self.model.objects.annotate(like_num=Count('likes')).order_by('-like_num')[:10]


# def index(request):
#     # 10 popular posts
#     posts = Post.objects.annotate(like_num=Count('likes')).order_by('-like_num')[:10]
#     return render(request, 'core/index.html', {'posts': posts, 'page_title': '10 posts'})


class FeedView(IndexView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            friends = self.request.user.profile.friends.all()
            return self.model.objects.filter(author__in=friends).annotate(like_num=Count('likes'))
        else:
            return None


# def feed(request):
#     # posts by friends
#     friends = request.user.profile.friends.all()
#     posts = Post.objects.filter(author__in=friends).annotate(like_num=Count('likes'))

#     return render(request, 'core/index.html', {'posts': posts, 'page_title': 'my firinds posts'})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, 'core/detail.html', {'post': post, 'page_title': 'Post detail'})


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/detail.html'
    comment_form = CommentForm

    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-date_pub')
        context['comment_form'] = self.comment_form

        return self.render_to_response(context)

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        form = self.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

        return render(request, self.template_name, {
            'post': post, 
            # 'comments': Comment.objects.filter(post=self.object).order_by('-date_pub')
            'comments': post.comment_set.order_by('-date_pub'),
            'comment_form': self.comment_form
            })



# def post_create(request):
#     if request.method == 'GET':
#         form = PostForm()
#         return render(request, 'core/post_create.html', {'form': form})
    
#     elif request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect(reverse('core:post_detail', kwargs={'post_id': post.id}))
#         else:
#             return render(request, 'core/post_create.html', {'form': form})
#     return HttpResponse('Post create')


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'core/post_create.html'
    login_url='/admin/login'

    # @method_decorator(login_required(login_url='/admin/login'))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('core:post_detail', kwargs={'post_id': post.id}))
        else:
            return render(request, 'core/post_create.html', {'form': form})
    

# def post_edit(request, post_id):
#     return HttpResponse('Post edit')


class EditView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_edit.html'
    form_class = PostForm

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('core:post_detail', args=(post_id, ))


# def post_delete(request, post_id):
#     return HttpResponse('Post delete')


class PostDelete(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_delete.html'
    # success_url = '/core/'

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('core:post_delete_success', args=(post_id, ))


# def like_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.user in post.likes.all():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)
#         post.save()

#     return redirect(request.META.get('HTTP_REFERER'), request)


class LikePostView(View):
    def get(self, request, post_id, *args, **kwargs):
        return redirect(reverse('core:post_detail', args=(post_id, )))

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            post.save()

        return redirect(request.META.get('HTTP_REFERER'), request)