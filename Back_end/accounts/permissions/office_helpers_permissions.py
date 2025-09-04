from rest_framework.permissions import BasePermission

from accounts.models import OfficeHelpersAccount


class IsOfficeHelper(BasePermission):
    """
    Allows access only to authenticated users who have a OfficeHelpers.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        print(request.user)
        return OfficeHelpersAccount.objects.filter(
            account__user=request.user
        ).exists()
