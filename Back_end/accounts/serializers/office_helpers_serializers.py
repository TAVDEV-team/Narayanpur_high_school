from rest_framework import serializers
from accounts.models import OfficeHelpersAccount
from .user_serializer import UserSerializer

class OfficeHelpersSerializer(serializers.ModelSerializer):
    account = UserSerializer()

    class Meta:
        model = OfficeHelpersAccount
        fields = [
            'id',
            'account',
            'designation',
        ]

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        user_serializer = UserSerializer(data=account_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return OfficeHelpersAccount.objects.create(account=user, **validated_data)
