from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=27)
    lunch_price = models.DecimalField(decimal_places=3)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name
# Create your models here.
