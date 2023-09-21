from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

class Invitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    email = models.TextField()  # Email as a text field
    token = models.TextField()  # Token as a text field
    ttl = models.DateTimeField(default=timezone.now)
    # Add other fields as needed

class Organization(models.Model):
    name = models.CharField(max_length=255)
    lunch_price = models.DecimalField(decimal_places=2, max_digits=10, null=False, default=0.00)
    currency = models.CharField(max_length=3, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Organizations'

class OrganizationLunchWallet(models.Model):
    """Model for Organization Lunch Wallet"""
    balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.balance}'
