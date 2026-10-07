from rest_framework.permissions import BasePermission

from accounts.models import TeacherAccount


class IsTeacher(BasePermission):
    """Allows access only to authenticated teachers."""

    def has_permission(self, request, view):
        return TeacherAccount.is_teacher(request.user)
