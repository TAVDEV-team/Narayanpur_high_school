from .headmaster_permission import IsHeadMaster
from .office_helpers_permissions import IsOfficeHelper
from .read_only import ReadOnlyOrRestricted
from .teacher_permission import IsTeacher
from .safe_headmaster_permissions import ISHeadmasterSafe

__all__ = [
    'IsHeadMaster',
    'IsTeacher',
    'IsOfficeHelper',
    'ReadOnlyOrRestricted',
    'ISHeadmasterSafe',
]
