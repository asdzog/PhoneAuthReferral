from django.urls import path

from api.views import UserCreateAPIView
from api.apps import ApiConfig

app_name = ApiConfig.name


urlpatterns = [
    path('create_user/', UserCreateAPIView.as_view(), name='create_user'),
]
