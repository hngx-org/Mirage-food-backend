
from django.db import models
from django.conf import settings
from users.models import User

class Lunch(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    redeemed = models.BooleanField(default=False)
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sender_id = models.ForeignKey(
        User,
        related_name="sent_lunches",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        User,
        related_name="received_lunches",
        on_delete=models.CASCADE,
    )
    """
        The related name can be used to query the database
        efficiently... eg
        To get all the lunches sent by the user - user.sent_lunches.all()
        To get all the lunches received by the user - user.received_lunches.all()
    """

    class Meta:
        verbose_name_plural = "Lunches"

    def __str__(self):
        return f"{self.sender} sent a lunch to {self.receiver}"
