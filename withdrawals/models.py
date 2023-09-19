from django.db import models

# Create your models here.
class Withdrawal(models.Model):
    status_choices = [
        ('pending', "processing"),
        ('completed', 'done')
    ]
    user_id = models.CharField(verbose_name='user ID', max_length=200)
    status = models.CharField(verbose_name='withdrawal status', choices=status_choices, max_length=20)
    amount = models.BigIntegerField(verbose_name='withdrawal amount')
    created_at = models.DateTimeField(verbose_name='withdrawal timestamp', auto_now_add=True)

    def __str__(self):
        return f"Withdrawal #{self.id}"