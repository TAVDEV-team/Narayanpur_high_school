from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from accounts.models import OfficeHelpersAccount
from accounts.serializers import OfficeHelpersSerializer


class OfficeHelpersAccountViewSet(ModelViewSet):
    queryset = OfficeHelpersAccount.objects.all()
    serializer_class = OfficeHelpersSerializer
    permission_classes = [AllowAny]
