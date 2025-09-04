from rest_framework import permissions

from .office_helpers_permissions import IsOfficeHelper
from .headmaster_permission import IsHeadMaster
from .teacher_permission import IsTeacher


class ReadOnlyOrRestricted(permissions.BasePermission):
    """
    Allow anyone to GET (safe methods).
    Restrict write actions (POST/PUT/PATCH/DELETE) to specific roles.
    """

    def has_permission(self, request, view):
        # SAFE methods = GET, HEAD, OPTIONS → always allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Otherwise → require at least one of the role permissions
        return (
            IsOfficeHelper().has_permission(request, view)
            or IsTeacher().has_permission(request, view)
            or IsHeadMaster().has_permission(request, view)
        )
