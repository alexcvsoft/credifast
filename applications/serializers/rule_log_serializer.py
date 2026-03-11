from rest_framework import serializers
from applications.models import RuleLog


class RuleLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = RuleLog
        fields = [
            "rule_name",
            "passed",
            "message"
        ]