from django.db import models

# Create your models here.


class User(models.Model):
    firstName = models.CharField(
        "First name", max_length=255, blank=True, null=True)
    lastName = models.CharField(
        "Last name", max_length=255, blank=True, null=True)

    username = models.CharField(
        "username", max_length=255, blank=True, null=True)    
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.firstName
