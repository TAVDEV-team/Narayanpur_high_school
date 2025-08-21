from rest_framework import serializers

from accounts.models import HeadMasterAccount

from .teacher_serializer import TeacherSerializer


class HeadMasterSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = HeadMasterAccount
        fields = ["teacher", "appointed_date"]
        depth = 0
