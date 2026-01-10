# from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from accounts.serializers import StudentListSerializer
from nphs_school.models import AClass, Subject

from .subject_serializer import SubjectListSerializer


class AClassReadSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()
    all_subjects = serializers.SerializerMethodField()

    class Meta:
        model = AClass
        fields = [
            "id",
            "name",
            "room_number",
            "students",
            "all_subjects",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_students(self, obj):
        return StudentListSerializer(
            obj.students().select_related("account"),
            many=True,
        ).data

    def get_all_subjects(self, obj):
        subjects = (
            list(obj.compulsory.all())
            + list(obj.group_subjects.all())
            + list(obj.religious.all())
            + list(obj.extra.all())
        )
        return SubjectListSerializer(subjects, many=True).data


class AClassSerializer(serializers.ModelSerializer):
    # students = StudentListSerializer(many=True, read_only=True)
    all_subjects = SubjectListSerializer(many=True, read_only=True)

    class Meta:
        model = AClass
        fields = [
            "id",
            "name",
            # "students",
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

    # def get_students(self, obj):
    #     return StudentListSerializer(
    #         obj.students().select_related("account"), many=True
    #     ).data


class AClassMetaSerializer(serializers.ModelSerializer):
    total_students = serializers.SerializerMethodField()
    male_students = serializers.SerializerMethodField()
    female_students = serializers.SerializerMethodField()

    class Meta:
        model = AClass
        fields = [
            "id",
            "name",
            "room_number",
            "total_students",
            "male_students",
            "female_students",
        ]

    def get_total_students(self, obj):
        return obj.students().count()

    def get_male_students(self, obj):
        return obj.students().filter(account__gender="male").count()

    def get_female_students(self, obj):
        return obj.students().filter(account__gender="female").count()


class AClassSubjectSerializer(serializers.ModelSerializer):
    all_subjects = SubjectListSerializer(many=True, read_only=True)

    class Meta:
        model = AClass
        fields = ["all_subjects"]
