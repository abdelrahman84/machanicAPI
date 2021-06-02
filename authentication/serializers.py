from rest_framework import serializers
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

#internal
from authentication.models import User



class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name',
			'username', 'email', 'phone', 'email_verified', 'token', 'password', 'createdAt')

	def create(self, validated_data):
		user = super(UserSerializer, self).create(validated_data)
		# user.password = make_password(validated_data['password'])
		# user.save()
		user.token = get_random_string(length=32)
		return user

