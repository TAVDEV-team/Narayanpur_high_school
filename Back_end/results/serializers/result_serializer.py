from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Result


class ResultSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True
    )
    class_name = serializers.CharField(
        source="aclass.__str__",
        read_only=True
    )
    mcq_max = serializers.IntegerField(
        source="subject.mcq_marks", read_only=True
    )
    written_max = serializers.IntegerField(
        source="subject.written_marks", read_only=True
    )
    practical_max = serializers.IntegerField(
        source="subject.practical_marks", read_only=True
    )
    student_name = serializers.CharField(
        source="student.account.full_name", read_only=True
    )
    student_roll = serializers.IntegerField(
        source="student.roll_number", read_only=True
    )

    class Meta:
        model = Result
        fields = [
            "class_name",
            'exam_type',
            "subject_name",
            "student_name",
            "student_roll",
            "mcq",
            "mcq_max",
            "practical",
            "practical_max",
            "written",
            "written_max",
            "total_marks",
            "percentage",
            "grade",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        student = attrs.get("student")
        subject = attrs.get("subject")
        exam_type = attrs.get("exam_type")
        aclass = student.batch.aclass

        if not aclass.subjects.filter(id=subject.id).exists():
            raise ValidationError("Invalid subject for this class")

        if Result.objects.filter(
            student=student, subject=subject, exam_type=exam_type
        ).exists():
            raise ValidationError("Result for this exam already exists.")

        return attrs
