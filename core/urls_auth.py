from django.urls.base import reverse_lazy
from django.urls.conf import path
from .views_auth import (
    LoginView, logout_view, ProfileView, AddRemoveFriends, EditProfileView, SignUpView
)
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/add_remove_friend', AddRemoveFriends.as_view(), name='add_remove_friend'),
    path('profile/<int:user_id>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password_reset/', PasswordResetView.as_view(success_url=reverse_lazy('core:password_reset_done'), template_name='my_auth/password_reset.html', email_template_name='my_auth/password_reset_email.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'password_reset/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('core:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path('password_reset/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]