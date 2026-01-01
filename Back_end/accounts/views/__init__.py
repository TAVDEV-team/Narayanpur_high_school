from .account_views import AccountViewSet, LogoutView
from .change_pass import ChangePasswordView
from .governing_views import GoverningBodyViewSet
from .headmaster_views import HeadMasterAccountViewSet
from .officehelpers_views import OfficeHelpersAccountViewSet
from .student_view import StudentAccountViewSet
from .teacher_views import TeacherAccountViewSet
from .custom_token_view import CustomTokenObtainPairView

__all__ = [
    'LogoutView',
    'HeadMasterAccountViewSet',
    'OfficeHelpersAccountViewSet',
    'StudentAccountViewSet',
    'TeacherAccountViewSet',
    'GoverningBodyViewSet',
    'AccountViewSet',
    'ChangePasswordView',
    'CustomTokenObtainPairView',
]
