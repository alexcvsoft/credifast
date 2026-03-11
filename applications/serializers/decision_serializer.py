from rest_framework import serializers
from applications.models import Decision
from .rule_log_serializer import RuleLogSerializer


class DecisionSerializer(serializers.ModelSerializer):

    rule_logs = RuleLogSerializer(many=True)

    class Meta:
        model = Decision
        fields = [
            "approved",
            "reason",
            "evaluated_at",
            "rule_logs"
        ]