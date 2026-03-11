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
        # Make the extracted fields read-only since they will be populated by the AI and not provided by the user
        extra_kwargs = {
            'extracted_name': {'read_only': True},
            'extracted_address': {'read_only': True},
            'extracted_date': {'read_only': True},
        }