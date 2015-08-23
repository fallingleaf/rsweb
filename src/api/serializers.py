from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'email')
        read_only_fields = ('email',)

class SignUpSerializer(serializers.Serializer):
    email     = serializers.EmailField()
    username  = serializers.CharField(max_length=128)
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)


    def validate_password2(self, value):
        passwd1 = self.initial_data['password1']
        passwd2 = value
        if passwd1 != passwd2:
            raise serializers.ValidationError("Passwords are not matched")
        return value

    def validate_email(self, value):
        try:
            user = UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            return value
        raise serializers.ValidationError("Email already exists")

    def validate_username(self, value):
        try:
            user = UserModel.objects.get(username=value)
        except UserModel.DoesNotExist:
            return value
        raise serializers.ValidationError("Username already exists")

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        passwd = self.validated_data['password1']
        user = UserModel.objects.create(username=username, email=email)
        user.set_password(passwd)
        user.is_active = True
        user.role = UserModel.USER_ROLE
        user.save()
        return user
