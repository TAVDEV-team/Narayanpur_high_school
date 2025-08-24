from .about_viewset import AboutViewSet
from .batch_view import BatchViewSet
from .class_view import AClassViewSet
from .notice_view import NoticeViewSet
from .routine_views import RoutineViewSet
from .school_view import SchoolViewSet
from .subject_view import SubjectViewSet
from .syllabus_views import SyllabusViewSet

__all__ = [
    'AboutViewSet',
    'AClassViewSet',
    'SchoolViewSet',
    'NoticeViewSet',
    'SubjectViewSet',
    'BatchViewSet',
    "RoutineViewSet",
    'SyllabusViewSet',
]
