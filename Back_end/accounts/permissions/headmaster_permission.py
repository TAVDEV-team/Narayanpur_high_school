from rest_framework.permissions import BasePermission

from accounts.models import HeadMasterAccount


class IsHeadMaster(BasePermission):
    """
    Allows access only to the currently assigned headmaster.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            headmaster = HeadMasterAccount.objects.get()
        except HeadMasterAccount.DoesNotExist:
            return False

        return request.user == headmaster.account.account.user
