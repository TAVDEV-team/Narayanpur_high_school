from rest_framework import serializers

from accounts.serializers import StudentSerializer
from nphs_school.models import (
    About,
    AClass,
    Batch,
    Notice,
    Routine,
    School,
    Subject,
    Syllabus,
)


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"


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


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class AClassSerializer(serializers.ModelSerializer):

    total_students = serializers.SerializerMethodField()
    male_students = serializers.SerializerMethodField()
    female_students = serializers.SerializerMethodField()
    students = StudentSerializer(many=True, read_only=True)

    all_subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = AClass
        fields = [
            "id",
            "name",
            "room_number",
            "total_students",
            "male_students",
            "female_students",
            "students",
            "all_subjects",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        # This will run `clean()` in model via `full_clean()` when saving
        # But we can add explicit validation to catch earlier
        errors = {}

        def check_subjects(subjects, allowed_types, field_name):
            wrong = [
                sub.name
                for sub in subjects
                if sub.subject_type not in allowed_types
            ]
            if wrong:
                errors[field_name] = [
                    f"{name} is not of allowed types {allowed_types}"
                    for name in wrong
                ]

        check_subjects(
            attrs.get("compulsory", []),
            [Subject.SubjectType.COMPULSORY],
            "compulsory",
        )
        check_subjects(
            attrs.get("group_subjects", []),
            [Subject.SubjectType.GROUP, Subject.SubjectType.GROUP_OPTIONAL],
            "group_subjects",
        )
        check_subjects(
            attrs.get("religious", []),
            [Subject.SubjectType.RELIGIOUS],
            "religious",
        )
        check_subjects(
            attrs.get("extra", []), [Subject.SubjectType.EXTRA], "extra"
        )

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        compulsory = validated_data.pop("compulsory", [])
        group_subjects = validated_data.pop("group_subjects", [])
        religious = validated_data.pop("religious", [])
        extra = validated_data.pop("extra", [])

        instance = AClass.objects.create(**validated_data)
        instance.compulsory.set(compulsory)
        instance.group_subjects.set(group_subjects)
        instance.religious.set(religious)
        instance.extra.set(extra)

        return instance

    def update(self, instance, validated_data):
        compulsory = validated_data.pop("compulsory", None)
        group_subjects = validated_data.pop("group_subjects", None)
        religious = validated_data.pop("religious", None)
        extra = validated_data.pop("extra", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if compulsory is not None:
            instance.compulsory.set(compulsory)
        if group_subjects is not None:
            instance.group_subjects.set(group_subjects)
        if religious is not None:
            instance.religious.set(religious)
        if extra is not None:
            instance.extra.set(extra)

        return instance

    def get_total_students(self, obj):
        return obj.students().count()

    def get_male_students(self, obj):
        return obj.students().filter(account__gender="male").count()

    def get_female_students(self, obj):
        return obj.students().filter(account__gender="female").count()


class RoutineSerializer(serializers.ModelSerializer):
    slot_display = serializers.CharField(
        source="get_slot_display", read_only=True
    )
    day_display = serializers.CharField(
        source="get_day_display", read_only=True
    )

    class Meta:
        model = Routine
        fields = "__all__" + ["slot_display", "day_display"]
        # ⚠️ "__all__" is not directly concatenable with lists, so fix below

        # Better approach:
        # fields = [
        #     "id",
        #     "aclass",
        #     "day",
        #     "day_display",
        #     "slot",
        #     "slot_display",
        #     "subject",
        #     "teacher",
        # ]


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
