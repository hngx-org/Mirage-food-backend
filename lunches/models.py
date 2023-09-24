
from django.db import models
from users.models import User
from organization.models import Organization

class Lunch(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    redeemed = models.BooleanField(default=False)
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sender_id = models.BigIntegerField()
    
    receiver_id = models.ForeignKey(
        User,
        related_name="received_lunches",
        on_delete=models.CASCADE,
    )
    org_id = models.ForeignKey(
        Organization,
        related_name='organization',
        on_delete=models.CASCADE
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
        return f"{self.sender_id} sent a lunch to {self.receiver_id}"
