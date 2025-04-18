from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    La clase CustomUserAdmin es una subclase de :class:`django.contrib.auth.admin.UserAdmin` para construir la
    interfaz del administrador con los campos cambiados del nuevo modelo de usuario llamado
    :class:`users.models.CustomUser`.
    """
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_verified',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_verified',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_verified')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
