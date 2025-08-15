from rest_framework.viewsets import ModelViewSet

from accounts.models import OfficeHelpersAccount
from accounts.serializers import OfficeHelpersSerializer


class OfficeHelpersAccountViewSet(ModelViewSet):
    queryset = OfficeHelpersAccount.objects.all()
    serializer_class = OfficeHelpersSerializer
