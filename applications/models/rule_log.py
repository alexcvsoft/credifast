from django.db import models
import uuid
from .decision import Decision


class RuleLog(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    decision = models.ForeignKey(
        Decision,
        on_delete=models.CASCADE,
        related_name="rule_logs"
    )

    rule_name = models.CharField(max_length=255)

    passed = models.BooleanField()

    message = models.TextField()    