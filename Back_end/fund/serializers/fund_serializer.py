from drf_spectacular.utils import extend_schema_field
from fund.models import Fund
from rest_framework import serializers


class FundSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Fund
        fields = [
            "id",
            "balance",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(str)
    def get_balance(self, obj):
        return obj.balance

    @extend_schema_field(str)
    def get_school_name(self, obj):
        return obj.school.name if obj.school else None
