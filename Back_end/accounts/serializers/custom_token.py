from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Account


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        # Auth-level check
        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            raise AuthenticationFailed("Account not found for this user.")

        # Domain-level check
        if not account.is_active:
            raise AuthenticationFailed("Account is inactive.")

        if not account.role:
            raise AuthenticationFailed("Account role is not assigned.")

        # Enrich response
        data["account_id"] = account.id
        data["role"] = account.role
        data["is_active"] = account.is_active

        return data
