import jwt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api import serializers
from api.utils import Utils
from core import settings
from users.models import CustomUser
from django.utils.translation import ugettext_lazy as _


class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(True)
        serializer.save()
        user_data = serializer.data

        saved_user = CustomUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(saved_user)
        Utils(request).validate_email_registration(saved_user.email, token)

        return Response(user_data, status=status.HTTP_201_CREATED)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.ChangePasswordSerializer


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        token = request.GET.get('token')
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(pk=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'message': _('Email correctamente verificado.')}, status=status.HTTP_200_OK)
            else:
                return Response({'message': _('Email ya se encontraba verificado.')}, status=status.HTTP_409_CONFLICT)
        except jwt.ExpiredSignatureError:
            return Response({'error': _('El correo de activación ha expirado.')}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': _('Token inválido')}, status=status.HTTP_400_BAD_REQUEST)


class ResendEmailConfirmationView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        email = request.GET.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = RefreshToken.for_user(user)
            Utils(request).validate_email_registration(user.email, token)
            return Response({'message': _('Nueva validación enviada correctamente')}, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response({'error': _('Email inválido')}, status=status.HTTP_400_BAD_REQUEST)

