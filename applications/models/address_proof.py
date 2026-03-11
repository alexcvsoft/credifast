from django.db import models
import uuid
from .application import Application


class AddressProof(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="address_proof"
    )

    file_url = models.CharField(max_length=500)

    extracted_name = models.CharField(max_length=255)
    extracted_address = models.CharField(max_length=255)

    extracted_date = models.DateField()