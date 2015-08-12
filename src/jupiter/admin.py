from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from models import AuthUser
from forms import AuthUserChangeForm, AuthUserCreationForm

class AuthUserAdmin(UserAdmin):
    form = AuthUserChangeForm
    add_form = AuthUserCreationForm

    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser')
        }),
    )

    search_fields = ('email', 'username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(AuthUser, AuthUserAdmin)

#admin.site.unregister(Group)