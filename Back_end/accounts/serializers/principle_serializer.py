from accounts.models import HeadMasterAccount
from rest_framework import serializers

from .teacher_serializer import TeacherSerializer


class HeadMasterSerializer(serializers.ModelSerializer):
    account = TeacherSerializer()

    class Meta:
        model = HeadMasterAccount
        fields = ["account", "appointed_date"]
        depth = 0
