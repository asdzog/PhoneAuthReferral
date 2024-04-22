import time

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
    @swagger_auto_schema(
        request_body=SendCodeSerializer,
        responses={200: 'Verification code sent', 400: 'Bad Request'}
    )
    def post(self, request):
        """Authorization by phone number.
                ---
                requestBody:
                  required: true
                  content:
                    application/json:
                      schema:
                        type: object
                        properties:
                          phone_number:
                            type: string
                            description: Номер телефона в формате "+7XXXXXXXXXX"
                            example: "+71234567890"
                responses:
                  '200':
                    description: Verification code sent
                  '400':
                    description: Bad Request
                """
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

            return Response(
                {'message': f'Confirmation code ({user.confirmation_code}) sent to user'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneAPIView(APIView):
    @swagger_auto_schema(
        request_body=VerifyPhoneSerializer,
        responses={200: 'Token created', 400: 'Bad Request'}
    )
    def post(self, request):
        """Phone number and confirmation code cheking  for creation JWT-token.
                ---
                requestBody:
                  required: true
                  content:
                    application/json:
                      schema:
                        type: object
                        properties:
                          phone_number:
                            type: string
                            description: Phone number using format like "+7XXXXXXXXXX"
                            example: "+71234567890"
                          confirmation_code:
                            type: string
                            description: Confirmation code
                            example: "1234"
                responses:
                  '200':
                    description: Token created
                    content:
                      application/json:
                        schema:
                          type: object
                          properties:
                            token:
                              type: string
                              description: JWT-token for user's authentication
                  '400':
                    description: Bad Request
                """
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
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: 'Успешный запрос', 403: 'Forbidden'}
    )
    def get(self, request):
        """Get user's profile."""
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


class ReferrerUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'invite_code': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={200: 'Successful updating of field "referrer"',
                   400: 'Invalid request or invite-code doesn\'t exist',
                   403: 'Forbidden'}
    )
    def put(self, request):
        """Updating user's field "referrer".
                    ---
                    requestBody:
                      required: true
                      content:
                        application/json:
                          schema:
                            type: object
                            properties:
                              invite_code:
                                type: string
                                description: Invite code for user, who should have that code
                                example: "ABC123"
                    responses:
                      '200':
                        description: Successful updating of field "referrer"
                      '400':
                        description: Invalid request or invite-code doesn't exist
                      '403':
                        description: Forbidden
                    """
        serializer = ProfileUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            invite_code = serializer.validated_data.get('invite_code')
            if User.objects.filter(invite_code=invite_code).exists():
                serializer.save()
                return Response({'detail': 'Поле "referrer" успешно обновлено'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Инвайт-код не существует'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
