from rest_framework import permissions

from accounts.models import HeadMasterAccount


class IsHeadmasterSafe(permissions.BasePermission):
    """
    Custom permission: Only HeadMaster can modify. But all can Read
    """

    def has_permission(self, request, view):
        # SAFE methods (GET/HEAD/OPTIONS) → allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            headmaster = HeadMasterAccount.objects.get()
        except HeadMasterAccount.DoesNotExist:
            return False
        return request.user == headmaster.teacher.account.user
