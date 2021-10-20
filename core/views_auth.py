from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.db.models import fields
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.views.generic.base import View
from .models import Profile
from .forms_auth import SignUpForm, UpdateProfileForm


from .forms_auth import LoginForm


class LoginView(DefaultLoginView):
    template_name = 'my_auth/login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('core:feed'), request)
            else:
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})



def logout_view(request):
    logout(request)
    return redirect(reverse('core:login'))


class ProfileView(DetailView):
    model = Profile
    template_name = 'my_auth/profile.html'

    def get_object(self):
        return get_object_or_404(self.model, user_id=self.kwargs['user_id'])


class AddRemoveFriends(View):
    def post(self, request, user_id, *args, **kwargs):
        profile = get_object_or_404(User, id=user_id)
        print(profile)
        if profile in request.user.profile.friends.all():
            request.user.profile.friends.remove(profile)
        else:
            request.user.profile.friends.add(profile)
        return redirect(request.META.get('HTTP_REFERER'), request)


class EditProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'my_auth/edit_profile.html'
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'

    def get_success_url(self):
        user_id = self.kwargs.get('user_id')
        return reverse('core:profile', args=(self.request.user.id, ))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise Http404('go away')
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)


class SignUpView(View):
    template_name = 'my_auth/signup.html'
    signup_form = SignUpForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.signup_form})

    def post(self, request, *args, **kwargs):
        user_form = self.signup_form(data=request.POST)

        registered = False
        
        context = {}
        if user_form.is_valid():
            user_form.save()
            registered = True
            context.update({'registered': registered})
        else:
            context.update({'form': user_form})
        
        

        return render(request, self.template_name, context)

