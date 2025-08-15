from rest_framework.permissions import BasePermission

from accounts.models import TeacherAccount


class IsTeacher(BasePermission):
    """
    Allows access only to authenticated users who have a TeacherAccount.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        print(request.user)
        return TeacherAccount.objects.filter(
            account__user=request.user
        ).exists()
