from .headmaster_permission import IsHeadMaster
from .office_helpers_permissions import IsOfficeHelper
from .read_only import ReadOnlyOrRestricted
from .safe_headmaster_permissions import IsHeadmasterSafe
from .teacher_permission import IsTeacher

__all__ = [
    'IsHeadMaster',
    'IsTeacher',
    'IsOfficeHelper',
    'ReadOnlyOrRestricted',
    'IsHeadmasterSafe',
]
