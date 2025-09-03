from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Result


class ResultSerializer(serializers.ModelSerializer):

    subject_name = serializers.CharField(source="subject.name", read_only=True)
    class_name = serializers.CharField(source="aclass.__str__", read_only=True)
    exam_title = serializers.CharField(
        source="exam.exam_title", read_only=True
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
            "id",
            "aclass",
            "class_name",
            "exam",
            "exam_title",
            "subject",
            "subject_name",
            "student",
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
        student = attrs.get("student") or getattr(
            self.instance, "student", None
        )
        subject = attrs.get("subject") or getattr(
            self.instance, "subject", None
        )
        exam = attrs.get("exam") or getattr(self.instance, "exam", None)

        if not student or not subject or not exam:
            raise ValidationError("Student, subject and exam are required.")

        # ✅ Exclude the current instance when checking duplicates
        qs = Result.objects.filter(student=student, subject=subject, exam=exam)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise ValidationError(
                {
                    "non_field_errors": [
                        f"Result for this {student} of {exam} already exists."
                    ]
                }
            )

        # 🔹 Subject max marks
        mcq_max = subject.mcq_marks or 0
        written_max = subject.written_marks or 0
        practical_max = subject.practical_marks or 0

        mcq = attrs.get("mcq", getattr(self.instance, "mcq", 0)) or 0
        written = (
            attrs.get("written", getattr(self.instance, "written", 0)) or 0
        )
        practical = (
            attrs.get("practical", getattr(self.instance, "practical", 0)) or 0
        )

        if mcq < 0 or mcq > mcq_max:
            raise ValidationError(
                {"mcq": f"Invalid MCQ mark: must be between 0 and {mcq_max}"}
            )
        if written < 0 or written > written_max:
            raise ValidationError(
                {
                    "written": (
                        "Invalid Written mark: must be between 0"
                        f"and {written_max}"
                    )
                }
            )
        if practical < 0 or practical > practical_max:
            raise ValidationError(
                {
                    "practical": (
                        "Invalid Practical mark: must be between 0"
                        f" and {practical_max}"
                    )
                }
            )

        # 🔹 Subject eligibility check
        aclass = student.batch.current_class
        if not (
            aclass.compulsory.filter(id=subject.id).exists()
            or aclass.group_subjects.filter(id=subject.id).exists()
            or aclass.religious.filter(id=subject.id).exists()
            or aclass.extra.filter(id=subject.id).exists()
        ):
            raise ValidationError(
                {
                    "subject": (
                        "This subject does not belong"
                        " to the student's class"
                    )
                }
            )

        return attrs
