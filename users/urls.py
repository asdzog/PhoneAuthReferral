from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    ProfileUpdateView, ConfirmAuthView, PhoneAuthView
)

app_name = UsersConfig.name

urlpatterns = [
    path('phone-auth/', PhoneAuthView.as_view(), name='phone-auth'),
    path('confirm-auth/', ConfirmAuthView.as_view(), name='confirm-auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile')
]
