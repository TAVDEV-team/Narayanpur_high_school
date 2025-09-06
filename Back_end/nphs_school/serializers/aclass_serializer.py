from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from accounts.serializers import StudentSerializer
from nphs_school.models import AClass, Subject

from .subject_serializer import SubjectSerializer


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

    @extend_schema_field(int)
    def get_total_students(self, obj) -> int:
        return obj.students().count()

    @extend_schema_field(int)
    def get_male_students(self, obj) -> int:
        return obj.students().filter(account__gender="male").count()

    @extend_schema_field(int)
    def get_female_students(self, obj) -> int:
        return obj.students().filter(account__gender="female").count()
