from rest_framework import serializers
from fund.models import Fund, FundTransaction

class FundSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    school_name = serializers.SerializerMethodField()
    class Meta:
        model = Fund
        fields = ['id', 'school', 'balance', 'created_at', 'updated_at','school_name']

    def get_balance(self, obj):
        return obj.balance
    def get_school_name(self, obj):
        return obj.school.name if obj.school else None

class FundTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundTransaction
        fields = '__all__'
        read_only_fields = ['after_transaction_balance']
