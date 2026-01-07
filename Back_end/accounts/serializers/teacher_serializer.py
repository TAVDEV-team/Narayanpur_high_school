from rest_framework import serializers

from accounts.models import TeacherAccount

from .account_serializer import AccountSerializer


class TeacherSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    base_subject_detail = serializers.SerializerMethodField()
    class_teacher_of_detail = serializers.SerializerMethodField()

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

    def get_base_subject_detail(self, obj):
        from nphs_school.serializers import SubjectSerializer

        return (
            SubjectSerializer(obj.base_subject).data
            if obj.base_subject
            else None
        )

    def get_class_teacher_of_detail(self, obj):
        from nphs_school.serializers import AClassSerializer

        return (
            AClassSerializer(obj.class_teacher_of).data
            if obj.class_teacher_of
            else None
        )

    def create(self, validated_data):
        account_data = validated_data.pop("account")
        account_serializer = AccountSerializer(data=account_data)
        account_serializer.is_valid(raise_exception=True)
        account = account_serializer.save()
        teacher = TeacherAccount.objects.create(
            account=account, **validated_data
        )
        return teacher


class TeacherListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="account.full_name", read_only=True
    )
    image = serializers.CharField(
        source="account.image", read_only=True
    )
    gender = serializers.CharField(
        source="account.get_gender_display", read_only=True
    )
    religion = serializers.CharField(
        source="account.get_religion_display", read_only=True
    )

    class Meta:
        model = TeacherAccount
        fields = [
            "id",
            "full_name",
            "gender",
            "religion",
            "image",
        ]
