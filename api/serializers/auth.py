from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Colaborador
from api.utils import Utils
from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': _("Los campos de contraseña no coinciden.")})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        _password2 = validated_data.pop('password2')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class FullRegisterSerializer(serializers.ModelSerializer):
    class ColaboradorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Colaborador
            ref_name = 'FullRegisterColaborador'
            fields = ['run', 'nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento',
                      'fecha_defuncion', 'sexo', 'estado_civil', 'nacionalidad', 'direccion', 'comuna', 'telefono_fijo',
                      'telefono_movil', 'email_personal', 'fecha_ingreso']

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    colaborador = ColaboradorSerializer()

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2', 'colaborador']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': _("Los campos de contraseña no coinciden.")})
        return attrs

    def create(self, validated_data):
        colaborador_data = validated_data.pop('colaborador')
        password = validated_data.pop('password')
        _password2 = validated_data.pop('password2')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        Colaborador.objects.create(usuario=user, **colaborador_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['old_password', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': _('Los campos de contraseña no coinciden.')})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': _('La contraseña antigua no es correcta.')})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ResendEmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(email=attrs['email'])
            token = RefreshToken.for_user(user)
            Utils(attrs['request']).validate_email_registration(user.email, token)
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': _('El correo electrónico no se encuentra en la base de datos')})


class ResetPasswordRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(email=attrs['email'])
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            name = user.colaborador.nombre if hasattr(user, 'colaborador') else ''
            Utils(attrs['request']).reset_password(user.email, uidb64, token, name)
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': _('El correo electrónico no se encuentra en la base de datos')})


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': _('Los campos de contraseña no coinciden.')})
        user = CustomUser.objects.get(pk=attrs['user_id'])
        user.set_password(attrs['password'])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        # data.update({'user_id': self.user.id})
        data.update({'user_email': self.user.email})

        return data
