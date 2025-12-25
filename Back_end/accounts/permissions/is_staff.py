from rest_framework import permissions


class IsStaff(permissions.BasePermission):
    """
    Custom permission: Only OfficeHelper, Teacher, or HeadMaster can modify.
    """

    def has_permission(self, request, view):
        # SAFE methods (GET/HEAD/OPTIONS) → allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Otherwise, must be staff
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (
                getattr(user, "is_office_helper", False)
                or getattr(user, "is_teacher", False)
                or getattr(user, "is_headmaster", False)
            )
        )
