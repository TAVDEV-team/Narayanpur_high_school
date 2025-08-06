from accounts.models import (
    HeadMasterAccount,
    OfficeHelpersAccount,
    StudentAccount,
    TeacherAccount,
)
from accounts.serializers import (
    HeadMasterSerializer,
    OfficeHelpersSerializer,
    StudentSerializer,
    TeacherSerializer,
)
from rest_framework.viewsets import ModelViewSet


class TeacherAccountViewSet(ModelViewSet):
    queryset = TeacherAccount.objects.all()
    serializer_class = TeacherSerializer


class StudentAccountViewSet(ModelViewSet):
    queryset = StudentAccount.objects.all()
    serializer_class = StudentSerializer


class OfficeHelpersAccountViewSet(ModelViewSet):
    queryset = OfficeHelpersAccount.objects.all()
    serializer_class = OfficeHelpersSerializer


class HeadMasterAccountViewSet(ModelViewSet):
    queryset = HeadMasterAccount.objects.all()
    serializer_class = HeadMasterSerializer
