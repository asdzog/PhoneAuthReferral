from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from users.models import User


class SendCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()


class VerifyPhoneSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    confirmation_code = serializers.CharField(max_length=4)


class ProfileViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'phone_number', 'invite_code', 'referrer')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ('name', 'phone_number', 'avatar', 'invite_code', 'referrer')
        read_only_fields = ('invite_code', 'phone_number', )
