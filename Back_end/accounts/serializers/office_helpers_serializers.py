from rest_framework import serializers

from accounts.models import OfficeHelpersAccount

from .account_serializer import AccountSerializer


class OfficeHelpersSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = OfficeHelpersAccount
        fields = [
            "id",
            "account",
            "designation",
        ]

    def create(self, validated_data):
        account_data = validated_data.pop("account")
        account_serializer = AccountSerializer(data=account_data)
        account_serializer.is_valid(raise_exception=True)
        account = account_serializer.save()
        teacher = OfficeHelpersAccount.objects.create(
            account=account, **validated_data
        )
        return teacher
