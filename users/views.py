from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from users.forms import UserProfileForm, PhoneAuthForm, ConfirmAuthForm
from users.models import User, UserManager


class UserLogout(LogoutView):
    model = User
    success_url = reverse_lazy('users:phone_auth')


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PhoneAuthView(View):
    def get(self, request):
        form = PhoneAuthForm()
        return render(request, 'users/phone_auth.html', {'form': form})

    def post(self, request):
        form = PhoneAuthForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            try:
                user = User.objects.get(phone_number=phone_number)
                user.confirmation_code = UserManager().generate_confirmation_code()
                user.save()
            except User.DoesNotExist:
                user = User.objects.create_user(phone_number=phone_number)
            return redirect('users:confirm-auth')
        return render(request, 'users/phone_auth.html', {'form': form})


class ConfirmAuthView(View):
    def get(self, request):
        form = ConfirmAuthForm()
        return render(request, 'users/confirm_auth.html', {'form': form})

    def post(self, request):
        form = ConfirmAuthForm(request.POST)
        if form.is_valid():  # kghkjgi
            # Проверяем введенный код подтверждения
            # Получаем введенный номер телефона и код подтверждения
            phone_number = form.cleaned_data['phone_number']
            entered_code = form.cleaned_data['confirmation_code']
            # Проверяем код подтверждения и авторизуем пользователя
            user, error_message = UserManager().check_confirmation_code_and_login(phone_number, entered_code)
            if user is not None:
                # Если код подтверждения правильный, авторизуем пользователя и перенаправляем на страницу профиля
                login(request, user)
                return redirect('users:profile')
            else:
                # Если код подтверждения неверный, возвращаем форму с ошибкой
                form.add_error('confirmation_code', error_message)
            # Если форма невалидна, возвращаем ее с ошибками
        return render(request, 'users/confirm_auth.html', {'form': form})
