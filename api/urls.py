from django.urls import path

from api.views import AuthAPIView, VerifyPhoneAPIView, UserProfileView
from api.apps import ApiConfig

app_name = ApiConfig.name


urlpatterns = [
    path('send-code/', AuthAPIView.as_view(), name='send_code'),
    path('verify-phone/', VerifyPhoneAPIView.as_view(), name='verify_phone'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
