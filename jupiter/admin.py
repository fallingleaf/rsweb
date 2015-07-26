from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from models import AuthUser

# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = AuthUser
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            AuthUser._default_manager.get(username=username)
        except AuthUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(comit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = AuthUser
        fields = ('email', 'password', 'username', 'is_staff', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.inital["password"]



class AuthUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
    )

    add_fields = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser')
        }),
    )

    search_fields = ('email', 'username',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(AuthUser, AuthUserAdmin)

#admin.site.unregister(Group)