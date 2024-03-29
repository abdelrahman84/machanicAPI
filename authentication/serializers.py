from rest_framework import serializers
from django.utils.crypto import get_random_string
from django.core import validators
import json as simplejson

# 3rd-party

# internal
from authentication.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'email_verified',
                  'verify_token', 'password', 'token', 'createdAt')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.verify_token = get_random_string(length=32)
        user.save()
        return user


class VerifyTokenSerializer(serializers.Serializer):

    verify_token = serializers.CharField(required=True)
    password = serializers.CharField(max_length=128, required=True, validators=[
        validators.RegexValidator(
            regex='^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,}$',
            message='Please enter a strong password'
        )
    ])


class VerifyLoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if self.user.email_verified:
            refresh = self.get_token(self.user)

            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            user = UserSerializer(self.user)

            data['user'] = simplejson.dumps(user.data)
            return data

        raise serializers.ValidationError('Please verify your email first')


class UpdateNameSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(max_length=128, required=True, validators=[
        validators.RegexValidator(
            regex='^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,}$',
            message='Please enter a strong password'
        )
    ])
