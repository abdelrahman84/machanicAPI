from django.core import validators
from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator

# Create your models here.


class User(models.Model):

    username_validatior = ASCIIUsernameValidator()

    first_name = models.CharField(
        "First name", max_length=255, blank=False, null=False)
    last_name = models.CharField(
        "Last name", max_length=255, blank=False, null=False)

    username = models.CharField(
        "username", max_length=255, blank=False, null=False, unique=True, validators=[username_validatior])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=False, null=False, validators=[
        validators.RegexValidator(
            regex='^(?=\d{11,}$)(01)\d',
            message='Please enter a valid number'
        )
    ])
    createdAt = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.first_name
