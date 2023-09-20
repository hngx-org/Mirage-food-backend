from django.db import models

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=27, blank=False)
    lunch_price = models.DecimalField(decimal_places=2)
    currency = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Organizations'


# A model to represent the wallet owned by an organization (according to the present schema)
class Organization_Lunch_Wallet(models.Model):
    org_id = models.OneToOneField(Organization, related_name='lunch_wallet', on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, default=0.00)

    def __str__(self):
        return self.org_id.__str__()