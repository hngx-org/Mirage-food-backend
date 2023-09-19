from django.db import models
from users.models import User

class Lunches(models.Model):
    sender = models.ForeignKey('Users', on_delete=models.CASCADE)
    receiver = models.ForeignKey('Users', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    redeemed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=128)



# Create your models here.
