from rest_framework import serializers

from fund.models import Fund, FundTransaction
from school_backend.logger import get_logger

logger = get_logger(__name__)


class FundTransactionSerializer(serializers.ModelSerializer):
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
            "created_at",
        ]
        read_only_fields = ["after_transaction_balance"]

    def validate_amount(self, value) -> int:
        if value <= 0:
            logger.info(f"{value} is rejected")
            raise serializers.ValidationError("Amount must be positive.")
        elif value > 100000000:
            logger.info(f"{value} invalid")
            raise serializers.ValidationError("Amount must be valid.")
        return value

    def validate(self, data) -> dict:
        fund = Fund.get_solo()
        if data["type"] == "EXPENSE" and data["amount"] > fund.balance:
            logger.warning(
                f"Rejected expense {data['amount']}\
                exceeding balance {fund.balance}"
            )
            raise serializers.ValidationError(
                "Not enough balance for this expense."
            )
        return data

    def validate_type(self, value) -> str:
        if value not in dict(FundTransaction.TRANSACTION_TYPES):
            raise serializers.ValidationError("Invalid transaction type.")
        return value
