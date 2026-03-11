from rest_framework import serializers
from applications.models import AddressProof


class AddressProofSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressProof
        fields = [
            "file_url",
            "extracted_name",
            "extracted_address",
            "extracted_date"
        ]