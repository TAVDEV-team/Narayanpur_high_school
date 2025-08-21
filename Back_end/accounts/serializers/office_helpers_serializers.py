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
