from fund.models import Fund, FundTransaction
from rest_framework import serializers


class FundTransactionSerializer(serializers.ModelSerializer):
    fund = Fund.get_solo()

    class Meta:
        model = FundTransaction
        fields = [
            "id",
            "type",
            "amount",
            "reason",
            "payment_method",
            "after_transaction_balance",
            "date",
        ]
        read_only_fields = ["after_transaction_balance"]

    def validate_amount(self, value) -> int:
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        elif value > 100000000:
            raise serializers.ValidationError("Amount must be valid.")
        return value

    def validate(self, data) -> str:
        if data["type"] == "EXPENSE" and data["amount"] > self.fund.balance:
            raise serializers.ValidationError(
                "Not enough balance for this expense."
            )
        return data

    def validate_type(self, value) -> int:
        if value not in dict(FundTransaction.TRANSACTION_TYPES):
            raise serializers.ValidationError("Invalid transaction type.")
        return value
