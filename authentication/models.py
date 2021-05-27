from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(
        "First name", max_length=255, blank=False, null=False)
    last_name = models.CharField(
        "Last name", max_length=255, blank=False, null=False)

    username = models.CharField(
        "username", max_length=255, blank=False, null=False, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=False, null=False)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.first_name
