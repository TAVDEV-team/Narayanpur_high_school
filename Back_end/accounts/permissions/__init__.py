from .headmaster_permission import IsHeadMaster
from .read_only import ReadOnlyOrRestricted
from .teacher_permission import IsTeacher
from .office_helpers_permissions import IsOfficeHelper

__all__ = [
    'IsHeadMaster',
    'IsTeacher',
    'IsOfficeHelper',
    'ReadOnlyOrRestricted',
]
