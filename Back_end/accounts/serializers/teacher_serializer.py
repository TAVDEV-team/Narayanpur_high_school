from rest_framework import serializers

from accounts.models import TeacherAccount
from nphs_school.serializers import AClassSerializer, Subjecterializer

from .account_serializer import AccountSerializer


class TeacherSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    base_subject_detail = Subjecterializer(
        source="base_subject", read_only=True
    )
    class_teacher_of_detail = AClassSerializer(
        source="class_teacher_of", read_only=True
    )

    class Meta:
        model = TeacherAccount
        fields = [
            "id",
            "account",
            "base_subject",
            "base_subject_detail",
            "is_class_teacher",
            "class_teacher_of",
            "class_teacher_of_detail",
        ]

    def validate(self, data):
        is_class_teacher = data.get("is_class_teacher")
        class_teacher_of = data.get("class_teacher_of")

        if is_class_teacher and not class_teacher_of:
            raise serializers.ValidationError(
                {
                    "class_teacher_of": "Must be \
                    set if is_class_teacher is True."
                }
            )
        return data

    def create(self, validated_data):
        account_data = validated_data.pop("account")

        account_serializer = AccountSerializer(data=account_data)
        account_serializer.is_valid(raise_exception=True)
        account = account_serializer.save()

        teacher = TeacherAccount.objects.create(
            account=account, **validated_data
        )
        return teacher

    def update(self, instance, validated_data):
        account_data = validated_data.pop("account", None)

        if account_data:
            for attr, value in account_data.items():
                setattr(instance.account, attr, value)
            instance.account.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
