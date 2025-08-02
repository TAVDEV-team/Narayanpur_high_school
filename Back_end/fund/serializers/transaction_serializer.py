from rest_framework import serializers
from fund.models import FundTransaction

class FundTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundTransaction
        fields = '__all__'
        read_only_fields = ['after_transaction_balance']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value
    
    def validate(self, data):
        if data["type"] == "EXPENSE" and data["amount"] > data["fund"].balance:
            raise serializers.ValidationError("Not enough balance for this expense.")
        return data
    
    def validate_type(self, value):
        if value not in dict(FundTransaction.TRANSACTION_TYPES):
            raise serializers.ValidationError("Invalid transaction type.")
        return value
