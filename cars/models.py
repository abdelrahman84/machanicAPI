from django.db import models


class Car(models.Model):
    
    name = models.CharField(max_length=255, blank=False, null=False)

    model = models.CharField(max_length=255, blank=False, null=False)

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)

    manufacturing_date = models.DateField(blank=True)

    total_distance = models.DecimalField(max_digits=64,decimal_places=2,blank=False)

    def __str__(self):
       return self.name   