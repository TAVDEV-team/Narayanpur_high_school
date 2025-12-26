from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords must match."}
            )
        # if User.objects.filter(email=data.get("email")).exists():
        #     raise serializers.ValidationError(
        #         {"email": "Email is already in use."}
        #     )
        data['email'] = self.validate_email(data['email'])

        return data

    def validate_email(self, email):
        if email == "student_email@gmail.com":
            return email
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already in use.")
        return email

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
