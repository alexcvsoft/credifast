from django.db import models
import uuid 
from .application import Application

class Decision(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="decision"
    )

    approved = models.BooleanField()
    reason = models.CharField(max_length=255)

    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Decision for {self.application.full_name}: {'Approved' if self.approved else 'Rejected'}"