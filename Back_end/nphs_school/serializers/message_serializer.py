from rest_framework import serializers

from accounts.models import TeacherAccount
from nphs_school.models import Messages


class MessageTeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="account.full_name", read_only=True
    )
    image = serializers.ImageField(source="account.image", read_only=True)

    class Meta:
        model = TeacherAccount
        fields = ["image", "full_name"]


class MessagesSerializer(serializers.ModelSerializer):
    message_of = MessageTeacherSerializer(read_only=True)

    class Meta:
        model = Messages
        fields = ["id", "message", "created_at", "updated_at", "message_of"]
