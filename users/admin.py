from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Class for update admin layout

    It's subclassing UserAdmin for build an admin layout similar to original with default user.
    """
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fieldsets': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        })
    )
    search_fields = ('email',)
    ordering = ('email',)
