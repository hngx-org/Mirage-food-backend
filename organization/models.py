from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=27, blank=False)
    lunch_price = models.DecimalField(decimal_places=2)
    currency = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Organizations'


# Create your models here.
