from django.db import transaction
from rest_framework import serializers

from accounts.models import Account

from .user_serializer import UserSerializer


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    display_gender = serializers.CharField(
        source='get_gender_display',
        read_only=True
        )
    display_religion = serializers.CharField(
        source='get_religion_display',
        read_only=True
        )

    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "image",
            "date_of_birth",
            "mobile",
            "religion",
            "display_religion",
            "gender",
            "display_gender",
            "address",
            "joining_date",
            "last_educational_institute",
            "full_name",
        ]
        read_only_fields = ["full_name"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = UserSerializer(
                instance=instance.user, data=user_data, partial=True
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        with transaction.atomic():
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            account = Account.objects.create(user=user, **validated_data)
        return account

    def validate_mobile(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile must be digits only.")
        if len(value) > 14:
            raise serializers.ValidationError(
                "Mobile must not exceed 14 digits."
            )
        return value
