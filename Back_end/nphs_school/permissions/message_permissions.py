from rest_framework.permissions import SAFE_METHODS, BasePermission


class MessagesPermission(BasePermission):
    """
    - Anyone can read (GET, HEAD, OPTIONS).
    - Only authenticated users with role 'teacher' can create/update/delete.
    """

    def has_permission(self, request, view):
        # Read-only actions are allowed for everyone
        if request.method in SAFE_METHODS:
            return True

        # Non-read actions → must be teacher
        return (
            request.user.is_authenticated
            and hasattr(
                request.user, "account"
            )  # if you have a related Account model
            and getattr(request.user.account, "role", None) == "teacher"
        )
