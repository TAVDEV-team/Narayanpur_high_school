from django.db import transaction
from rest_framework import serializers

from accounts.models import StudentAccount

from .account_serializer import AccountSerializer


class StudentSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = StudentAccount
        fields = [
            "batch",
            "group",
            "roll_number",
            "account",
        ]
        read_only_fields = ["roll_number"]

    def create(self, validated_data):
        account_data = validated_data.pop("account")
        with transaction.atomic():
            account_serializer = AccountSerializer(data=account_data)
            account_serializer.is_valid(raise_exception=True)
            account = account_serializer.save()
            student = StudentAccount.objects.create(
                account=account, **validated_data
            )
        return student

    def update(self, instance, validated_data):
        account_data = validated_data.pop("account", None)
        if account_data:
            account_serializer = AccountSerializer(
                instance=instance.account, data=account_data, partial=True
            )
            account_serializer.is_valid(raise_exception=True)
            account_serializer.save()

        return super().update(instance, validated_data)
