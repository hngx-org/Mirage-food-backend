from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 

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
    # Add other fields as needed

    def __str__(self):
        return self.name