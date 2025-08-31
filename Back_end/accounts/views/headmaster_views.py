from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from accounts.models import HeadMasterAccount
from accounts.serializers import HeadMasterSerializer


class HeadMasterAccountViewSet(ModelViewSet):
    queryset = HeadMasterAccount.objects.all()
    serializer_class = HeadMasterSerializer
    permission_classes = [AllowAny]
