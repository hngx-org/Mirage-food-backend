from django.db import models
from users.models import User

# Create your models here.
class Withdrawal(models.Model):
    status_choices = [
        ('redeemed', "Redeemed"),
        ('not_redeemed', 'Not Redeemed'),
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='withdrawal status', choices=status_choices, max_length=20,default='not_redeemed')
    amount = models.DecimalField(verbose_name='withdrawal amount',max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(verbose_name='withdrawal timestamp', auto_now_add=True)
    updated_at=models.DateTimeField(verbose_name='updated timestamp',auto_now=True)
    def __str__(self):
        return f"Withdrawal #{self.id}"