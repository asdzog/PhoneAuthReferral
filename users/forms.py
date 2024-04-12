from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms


from users.models import User, UserManager


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'


class PhoneAuthForm(forms.Form):
    phone_number = forms.CharField(label='Номер телефона', max_length=15)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Проверяем, существует ли пользователь с указанным номером телефона
        try:
            user = User.objects.get(phone_number=phone_number)
            # Пользователь уже существует, создаем новый код подтверждения
            user.confirmation_code = UserManager().generate_confirmation_code()
            user.save()
        except User.DoesNotExist:
            # Пользователя с таким номером телефона не существует, создаем нового пользователя
            user = User.objects.create_user(phone_number=phone_number)
        return phone_number


class ConfirmAuthForm(forms.Form):
    confirmation_code = forms.CharField(label='Confirmation Code', max_length=4, required=True)
    phone_number = forms.CharField(widget=forms.HiddenInput())


class UserProfileForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'avatar', 'confirmation_code', 'invite_code', 'invited_users')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
