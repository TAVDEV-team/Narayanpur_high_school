from django.db import transaction
from rest_framework import serializers

from accounts.models import StudentAccount
from nphs_school.models import AClass

from .account_serializer import AccountSerializer


class StudentSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    class_name = serializers.CharField(write_only=True)
    group = serializers.CharField(write_only=True, default="science")

    batch_label = serializers.CharField(source="batch.label", read_only=True)
    aclass = serializers.SerializerMethodField()

    class Meta:
        model = StudentAccount
        fields = [
            "id",
            "class_name",
            "group",
            "aclass",
            "batch_label",
            "roll_number",
            "account",
        ]
        read_only_fields = ["roll_number", "aclass", "batch_label"]

    def get_aclass(self, obj):
        aclass = obj.batch.current_class
        return str(aclass) if aclass else None

    def create(self, validated_data):
        account_data = validated_data.pop("account")
        aclass_id = validated_data.pop("class_name")

        group_map = {
            "9": {
                "science": "9_science",
                "business": "9_business",
                "humanities": "9_humanities",
            },
            "10": {
                "science": "10_science",
                "business": "10_business",
                "humanities": "10_humanities",
            },
        }
        if aclass_id in group_map:
            aclass_name = group_map[aclass_id].get(validated_data["group"])
        else:
            aclass_name = aclass_id
        aclass = AClass.objects.get(name=aclass_name)

        with transaction.atomic():
            last_roll = (
                StudentAccount.objects.select_for_update()
                .filter(batch=aclass.batch)
                .order_by("-roll_number")
                .first()
            )
            number = (last_roll.roll_number + 1) if last_roll else 1
            user_name = (
                f"{str(aclass.batch).replace("-", "_").lower()}{number}"
            )

            # normalize dummy email + username
            account_data["user"]["username"] = user_name
            if account_data["user"]["email"] == "dummy_email@gmail.com":
                account_data["user"][
                    "email"
                ] = f"{user_name.lower()}@gmail.com"

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

            # finally create student
            student = StudentAccount.objects.create(
                account=account, batch=batch, **validated_data
            )

        return student
