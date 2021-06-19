from rest_framework import serializers
from django.utils.crypto import get_random_string
from django.core import validators

# 3rd-party

#internal
from authentication.models import User



class UserSerializer(serializers.ModelSerializer):

	token = serializers.CharField(max_length=255,read_only=True)
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name',
			'username', 'email', 'phone', 'email_verified', 'verify_token', 'password', 'token', 'createdAt')

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

