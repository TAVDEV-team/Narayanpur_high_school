from rest_framework import serializers

from nphs_school.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    total_marks = serializers.IntegerField(read_only=True)

    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "subject_type",
            "code",
            "written_marks",
            "practical_marks",
            "mcq_marks",
            "total_marks",
        ]
