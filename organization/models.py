from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    lunch_price = models.DecimalField(
        decimal_places=2, max_digits=10, null=False, default=0.00)
    currency = models.CharField(max_length=3, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Organizations'


class OrganizationLunchWallet(models.Model):
    """Model for Organization Lunch Wallet"""
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.balance}'
