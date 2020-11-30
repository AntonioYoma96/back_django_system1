from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom manager for the change of username to email as unique identifier for authentication

    It's subclassing BaseUserManager for the minimum changes in the user structure.
    """

    def create_user(self, email, password, **extra_fields):
        """Function for the custom manager that creates standard user

        :param email: Email for the new user
        :param password: Password for the new user
        :param extra_fields: Other fields of user model for his creation
        :return: New user model
        """
        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Function for the custom manager that creates super user.

        This function also specifies superuser roles like is_staff, is_superuser and is active.

        :param email: Email for the new superuser
        :param password: Password for the new superuser
        :param extra_fields: Other fields of user model for his creation
        :return: New user model (calling create_user method)
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Class for the new user

    It's subclassing AbstractUser for the minimum changes in the user model.
    """
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """Function that send a formatted version of CustomUser

        :return: String of user's emails
        """
        return self.email
