import time

from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import AuthSerializer
from users.models import User
from users.managers import CustomUserManager



