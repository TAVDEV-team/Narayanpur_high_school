from rest_framework import serializers

from accounts.models import GoverningBody

from .account_serializer import AccountSerializer


class GoverningBodySerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = GoverningBody
        fields = ["id", "account", "designation", "profession"]
