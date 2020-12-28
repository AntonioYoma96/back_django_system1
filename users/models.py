from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    La clase CustomUserManager es una subclase de :class:`django.contrib.auth.base_user.BaseUserManager` para editar
    los atajos de Django de creación de usuarios.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Función para la creación de usuarios con el administrador de Django.

        :param email: Email para el nuevo usuario.
        :param password: Contraseña del nuevo usuario.
        :param extra_fields: Arreglo con otros campos del usuario.
        :return: El modelo del nuevo :class:`CustomUser` creado.
        """
        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Función para la creación de super usuarios con el administrador de Django.

        :param email: Email para el nuevo super usuario.
        :param password: Contraseña del nuevo super usuario.
        :param extra_fields: Arreglo con otros campos del super usuario.
        :return: El modelo del nuevo :class:`CustomUser` creado (llamando la función :func:`create_user`)
        :raise
            :ValueError: Errores de incoherencias con la creación de super usuarios.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    La clase CustomUser es una subclase de :class:`django.contrib.auth.models.AbstractUser` que reemplaza el modelo
    de usuario de defecto de Django, para establecer campos necesarios para el sistema.

    Los cambios más importantes al modelo están representados en los siguientes parámetros:

    :param username: Pasa a estar vacío, ya que se usará otro campo como identificador de acceso al sistema.
    :param first_name: Pasa a estar vacío, ya que no es necesario en el sistema.
    :param last_name: Pasa a estar vacío, ya que no es necesario en el sistema.
    :param email: Campo de tipo texto para el usuario del sistema. Este será el nuevo identificador de acceso (incluye
        validación de email, único).
    :param USERNAME_FIELD: Este campo define el identificador del sistema, cambiado a :attr:`email`.
    """
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(
        _('verificado'),
        default=False,
        help_text=_('indica si el usuario ha verificado el email.')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con el email del usuario.
        """
        return self.email
