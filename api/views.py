import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import SendCodeSerializer, VerifyPhoneSerializer, ProfileViewSerializer, ProfileUpdateSerializer
from users.models import User
from users.permissions import IsOwner
from rest_framework.response import Response
from rest_framework import status
from users.utils import generate_confirmation_code, imitate_code_sending


class AuthAPIView(APIView):
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user, created = User.objects.get_or_create(phone_number=phone_number)

            # генерируем новый код подтверждения
            user.confirmation_code = generate_confirmation_code()
            user.save()

            # задержка времени 2 сек
            time.sleep(2)

            # имитация отправки кода подтверждения
            imitate_code_sending(phone_number, user.confirmation_code)

            return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneAPIView(APIView):
    def post(self, request):
        serializer = VerifyPhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            confirmation_code = serializer.validated_data['confirmation_code']
            try:
                user = User.objects.get(phone_number=phone_number, confirmation_code=confirmation_code)
            except User.DoesNotExist:
                return Response({'error': 'Invalid phone number or confirmation code'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Создание JWT-токена
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Получаем список приглашенных пользователей для текущего пользователя
        invited_users = User.objects.filter(referrer=user.invite_code)
        # Получаем остальную информацию о пользователе
        serializer = ProfileViewSerializer(user)
        # Добавляем список приглашенных пользователей в данные пользователя
        data = serializer.data
        invited_users_data = ProfileViewSerializer(invited_users, many=True).data
        data['invited_users'] = invited_users_data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
