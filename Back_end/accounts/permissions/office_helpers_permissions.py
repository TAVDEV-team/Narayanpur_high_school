from rest_framework.permissions import BasePermission

from accounts.models import OfficeHelpersAccount


class IsOfficeHelper(BasePermission):
    """
    Allows access only to the currently assigned headmaster.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            headmaster = OfficeHelpersAccount.objects.get()
        except OfficeHelpersAccount.DoesNotExist:
            return False
        return request.user == headmaster.teacher.account.user
