from rest_framework import serializers
from applications.models import Application

# Defines how the Application model is serialized to JSON for API responses and deserialized from JSON for API requests.
class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = [
            "id",
            "full_name",
            "age",
            "is_married",
            "has_children",
            "monthly_income",
            "declared_address",
            "bank_history_months",
            "credit_score",
            "created_at",
        ]

        read_only_fields = ["id", "created_at"]