from django.db import models
import uuid

class Application(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    full_name = models.CharField(max_length=255)
    age = models.IntegerField()

    is_married = models.BooleanField()
    has_children = models.BooleanField()

    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)

    declared_address = models.CharField(max_length=255)

    bank_history_months = models.IntegerField()

    credit_score = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name