from rest_framework import serializers
from accounts.models import GoverningBody


class GoverningBodySerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(read_only=True)
    head_master = serializers.SerializerMethodField()

    class Meta:
        model = GoverningBody
        fields = ["id", "designation", "account", "head_master"]

    def get_head_master(self, obj):
        from .principle_serializer import HeadMasterSerializer
        return HeadMasterSerializer(
            obj.head_master
            ).data if obj.head_master else None
