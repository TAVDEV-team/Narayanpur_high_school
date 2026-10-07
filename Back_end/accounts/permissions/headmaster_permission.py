from rest_framework.permissions import BasePermission

from accounts.models import HeadMasterAccount


class IsHeadMaster(BasePermission):
    """Allows access only to the currently assigned headmaster."""

    def has_permission(self, request, view):
        return HeadMasterAccount.is_headmaster(request.user)
