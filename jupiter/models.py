from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AuthUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        """
        Create and save user with the given email, username and password
        :param email:
        :param username:
        :param password:
        :return: user
        """
        if not email:
            raise ValueError('Users must have email address')

        if not username:
            raise ValueError('Users must have username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.is_active = True
        user.set_password(password)
        user.role = AuthUser.USER_ROLE
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Create superuser with username, email and password
        :param username:
        :param email:
        :param password:
        :return: user
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.role = AuthUser.ADMIN_ROLE
        user.save(using=self._db)
        return user


class AuthUser(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'

    ROLES = (
        (USER_ROLE, 'User'),
        (ADMIN_ROLE, 'Admin'),
    )

    role = models.CharField(
        max_length=30,
        choices=ROLES,
        default=USER_ROLE,
    )

    objects = AuthUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.username

    def get_username(self):
        return self.USERNAME_FIELD

    def has_perm(self, perm, obj=None):
        # grant all permissions
        return True

    def has_module_perms(self, app_lable):
        return True

    def __unicode__(self):
        return self.email






