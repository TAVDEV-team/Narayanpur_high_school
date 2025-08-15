from rest_framework.viewsets import ModelViewSet

from accounts.models import StudentAccount
from accounts.serializers import StudentSerializer


class StudentAccountViewSet(ModelViewSet):
    queryset = StudentAccount.objects.all()
    serializer_class = StudentSerializer
