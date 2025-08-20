from rest_framework import serializers

from accounts.models import GoverningBody
from accounts.serializers import HeadMasterSerializer

from .account_serializer import AccountSerializer


class GoverningBodySerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    head_master = HeadMasterSerializer(read_only=True)

    class Meta:
        model = GoverningBody
        fields = ["id", "designation", "account", "head_master"]
