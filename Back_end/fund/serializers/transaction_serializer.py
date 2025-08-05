from rest_framework import serializers
from fund.models import FundTransaction, Fund
class FundTransactionSerializer(serializers.ModelSerializer):
    fund = Fund.objects.get(id=1)
    class Meta:
        model = FundTransaction
        fields = [
            'id',
            'type',
            'amount',
            'reason',
            'payment_method',
            'after_transaction_balance',
            'date'
        ]
        read_only_fields = ['after_transaction_balance']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value
    
    def validate(self, data):
        if data["type"] == "EXPENSE" and data["amount"] > self.fund.balance:
            raise serializers.ValidationError("Not enough balance for this expense.")
        return data
    
    def validate_type(self, value):
        if value not in dict(FundTransaction.TRANSACTION_TYPES):
            raise serializers.ValidationError("Invalid transaction type.")
        return value
