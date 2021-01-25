from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from api import serializers
from api.utils import Utils
from users.models import CustomUser


def send_validation_email(email, request):
    saved_user = CustomUser.objects.get(email=email)
    token = RefreshToken.for_user(saved_user)
    Utils(request).validate_email_registration(saved_user.email, token)


class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        user = request.data
        print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(True)
        serializer.save()
        user_data = serializer.data

        send_validation_email(user_data['email'], request)

        return Response(user_data, status=status.HTTP_201_CREATED)


class FullRegisterView(generics.GenericAPIView):
    serializer_class = serializers.FullRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        registration = request.data
        serializer = self.serializer_class(data=registration)
        serializer.is_valid(True)
        serializer.save()
        user_data = serializer.data

        send_validation_email(user_data['email'], request)

        return Response(user_data, status=status.HTTP_201_CREATED)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.ChangePasswordSerializer


class VerifyEmailView(APIView):
    @staticmethod
    def get(request):
        user = CustomUser.objects.get(pk=request.user.id)
        if not user.is_verified:
            user.is_verified = True
            user.save()
            return Response({'message': _('Email correctamente verificado.')}, status=status.HTTP_200_OK)
        else:
            return Response({'message': _('Email ya se encontraba verificado.')}, status=status.HTTP_409_CONFLICT)


class ResendEmailConfirmationView(generics.GenericAPIView):
    serializer_class = serializers.ResendEmailConfirmationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = CustomUser.objects.get(email=request.data['email'])
            token = RefreshToken.for_user(user)
            Utils(request).validate_email_registration(user.email, token)
            return Response(
                {'message': _('Nueva validación de correo enviada correctamente')},
                status=status.HTTP_202_ACCEPTED
            )
        except ObjectDoesNotExist:
            return Response(
                {'error': _('El correo electrónico no se encuentra en la base de datos')},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ResetPasswordRequestView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = CustomUser.objects.get(email=request.data["email"])
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            name = user.colaborador.nombre if hasattr(user, 'colaborador') else ''
            Utils(request).reset_password(user.email, uidb64, token, name)
            return Response(
                {'message': _('Email con instrucciones de cambio de contraseña enviado correctamente')},
                status=status.HTTP_202_ACCEPTED
            )
        except ObjectDoesNotExist:
            return Response(
                {'error': _('El correo electrónico entregado no existe en la base de datos')},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(_('El token para cambio de contraseña es invalido'), 401)

            data = {
                'user_id': user.id,
                'password': request.data['password'],
                'password2': request.data['password2']
            }
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(
                {'message': _('Contraseña cambiada correctamente')},
                status=status.HTTP_202_ACCEPTED
            )
        except ValueError:
            return Response(
                {'error': _('Error en la codificación del identificador del usuario')}
            )


class CustomTokenObtainPairView(TokenViewBase):
    serializer_class = serializers.CustomTokenObtainPairSerializer
