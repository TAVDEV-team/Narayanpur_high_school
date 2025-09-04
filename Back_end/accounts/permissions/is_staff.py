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


# from rest_framework import permissions
# from accounts.models import OfficeHelpersAccount, TeacherAccount
# import accounts.models.teacher import HeadMasterAccount


# class IsStaff(permissions.BasePermission):
#     """
#     Allow everyone to read (GET/HEAD/OPTIONS).
#     Only OfficeHelper, Teacher, or HeadMaster accounts can modify.
#     """

#     def has_permission(self, request, view):
#         # SAFE methods = read-only
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         if not request.user or not request.user.is_authenticated:
#             return False

#         user = request.user

#         return (
#             OfficeHelpersAccount.objects.filter(account__user=user).exists()
#             or TeacherAccount.objects.filter(account__user=user).exists()
#             or HeadmasterAccount.objects.filter(account__user=user).exists()
#         )
