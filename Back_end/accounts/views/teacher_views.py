from rest_framework.viewsets import ModelViewSet

from accounts.models import TeacherAccount
from accounts.serializers import TeacherSerializer


class TeacherAccountViewSet(ModelViewSet):
    queryset = TeacherAccount.objects.all()
    serializer_class = TeacherSerializer
