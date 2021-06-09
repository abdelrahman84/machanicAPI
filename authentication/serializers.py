from rest_framework import serializers
from django.utils.crypto import get_random_string
from django.core import validators

#internal
from authentication.models import User



class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name',
			'username', 'email', 'phone', 'email_verified', 'token', 'password', 'createdAt')

	def create(self, validated_data):
		user = super(UserSerializer, self).create(validated_data)
		user.token = get_random_string(length=32)
		user.save()
		return user

class VerifyTokenSerializer(serializers.Serializer):

	token = serializers.CharField(required=True)
	password = serializers.CharField(max_length=128, required=True, validators=[
		validators.RegexValidator(
			regex='^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,}$',
			message='Please enter a strong password'
		)
	])
