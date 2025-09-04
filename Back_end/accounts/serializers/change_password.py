from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user

        # 1. old password check
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Wrong password."}
            )

        # 2. confirm password match
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        # 3. new password strength validation
        validate_password(attrs["new_password"], user)

        return attrs
