from rest_framework import serializers

from nphs_school.models import Syllabus


class SyllabusSerializer(serializers.ModelSerializer):
    class_title = serializers.CharField(source="aclass.name", read_only=True)

    class Meta:
        model = Syllabus
        fields = [
            "id",
            "aclass",
            "class_title",
            "title",
            "file",
            "uploaded_at",
        ]
