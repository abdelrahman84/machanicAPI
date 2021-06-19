from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from django.db import models
from django.core import validators

# 3rd party

import jwt

class UserManager(BaseUserManager):

	def create_user(self, username, email, password):

		if username is None:
			raise TypeError('username is missing')

		if email is None:
			raise TypeError('email is missing')

		user = self.model(username=username, email=email)
		user.set_password(password)
		user.save()

		return user 

	def create_superuser(self, username, email, password):

		if username is None:
			raise TypeError('username is missing')

		if email is None:
			raise TypeError('email is missing')

		if password is None:
			raise TypeError('password is missing') 

		user = self.create_user(username, email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save()

		return user

class User(AbstractUser):

	first_name = models.CharField(
		"First name", max_length=255, blank=False, null=False)
	last_name = models.CharField(
		"Last name", max_length=255, blank=False, null=False)

	username = models.CharField(
		"username", max_length=255, blank=False, null=False, unique=True)

	email = models.EmailField(unique=True)

	phone = models.CharField(max_length=225, blank=True, null=False, validators=[
		validators.RegexValidator(
			regex='^(?=\d{11,}$)(01)\d',
			message='Please enter a valid number'
		)
	])

	verify_token = models.CharField(max_length=225, blank=True, null=False)

	email_verified = models.BooleanField(default=False)

	password = models.CharField(max_length=128, blank=True, null=False, validators=[
		validators.RegexValidator(
			regex='^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,}$',
			message='Please enter a strong password'
		)
	])

	is_active = models.BooleanField(default=True)

	is_staff = models.BooleanField(default=False)

	createdAt = models.DateTimeField("Created At", auto_now_add=True)

	updated_at = models.DateTimeField("Updated At", auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = UserManager()

	def __str__(self):

		return self.email 


