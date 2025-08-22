from django.db import transaction
from rest_framework import serializers

from accounts.models import StudentAccount
from nphs_school.models import AClass

from .account_serializer import AccountSerializer


class StudentSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    aclass_id = serializers.PrimaryKeyRelatedField(
        queryset=AClass.objects.all(), write_only=True
    )
    aclass = serializers.CharField(source="class", read_only=True)
    batch_label = serializers.CharField(source="batch.label", read_only=True)

    class Meta:
        model = StudentAccount
        fields = [
            "aclass_id",
            "aclass",
            "batch_label",
            "group",
            "roll_number",
            "account",
        ]
        read_only_fields = ["roll_number", "aclass", "batch_label"]

    def create(self, validated_data):
        account_data = validated_data.pop("account")
        aclass = validated_data.pop("aclass_id")

        with transaction.atomic():
            last_roll = (
                StudentAccount.objects.select_for_update()
                .filter(batch=aclass.batch)
                .order_by("-roll_number")
                .first()
            )
            number = (last_roll.roll_number + 1) if last_roll else 1
            user_name = f"{str(aclass.batch)}{number}"
            account_data['user']['username'] = user_name
            # create account first
            account_serializer = AccountSerializer(data=account_data)
            account_serializer.is_valid(raise_exception=True)
            account = account_serializer.save()

            # resolve batch from class
            batch = aclass.batch
            if not batch:
                raise serializers.ValidationError(
                    "This class has no batch assigned."
                )

            student = StudentAccount.objects.create(
                account=account, batch=batch, **validated_data
            )

        return student
