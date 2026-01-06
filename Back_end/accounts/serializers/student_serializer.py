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
        read_only_fields = ["aclass", "batch_label"]

    def get_aclass(self, obj):
        aclass = obj.batch.current_class
        return str(aclass) if aclass else None

    def create(self, validated_data):
        account_data = validated_data.pop("account")
        aclass_id = validated_data.pop("class_name")
        group_map = {
            "9": {
                "science": "9_science",
                "business studies": "9_business",
                "humanities": "9_humanities",
            },
            "10": {
                "science": "10_science",
                "business studies": "10_business",
                "humanities": "10_humanities",
            },
        }
        if aclass_id in group_map:
            aclass_name = group_map[aclass_id].get(validated_data["group"])
        else:
            aclass_name = aclass_id
        aclass = AClass.objects.get(name=aclass_name)
        roll_number = validated_data.pop('roll_number')
        with transaction.atomic():
            if roll_number is None:
                last_roll = (
                    StudentAccount.objects.select_for_update()
                    .filter(batch=self.batch, group=self.group)
                    .order_by("-roll_number")
                    .first()
                )
                roll_number = (last_roll.roll_number + 1) if last_roll else 1
            group = validated_data['group']
            if group:
                user_name = f"{str(aclass.batch).replace("-", "_").lower()}_{group[0]}_{account_data['religion'][0]}{account_data['gender'][0]}{account_data['user']['first_name'][0:1]}{account_data['user']['last_name'][0:1]}_{roll_number}"  # noqa: E501
            else:
                user_name = f"{str(aclass.batch).replace("-", "_").lower()}_{account_data['religion'][0]}{account_data['gender'][0]}{account_data['user']['first_name'][0:1]}{account_data['user']['last_name'][0:1]}_{roll_number}"  # noqa: E501
            validated_data['roll_number'] = roll_number
            # normalize dummy email + username
            account_data["user"]["username"] = user_name
            if account_data["user"]["email"] == "student_email@gmail.com":
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


class StudentListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="account.full_name", read_only=True
    )
    aclass = serializers.SerializerMethodField()
    # batch_label = serializers.CharField(source="batch.label", read_only=True)
    gender = serializers.CharField(
        source="account.get_gender_display", read_only=True
    )
    religion = serializers.CharField(
        source="account.get_religion_display", read_only=True
    )

    class Meta:
        model = StudentAccount
        fields = [
            "id",
            "full_name",
            "roll_number",
            # "group",
            "aclass",
            # "batch_label",
            "gender",
            "religion",
        ]

    def get_aclass(self, obj):
        aclass = obj.batch.current_class
        return str(aclass) if aclass else None
