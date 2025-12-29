from rest_framework import viewsets
from accounts.permissions import IsHeadmasterSafe

from accounts.models import GoverningBody
from accounts.serializers import GoverningBodySerializer


class GoverningBodyViewSet(viewsets.ModelViewSet):
    queryset = GoverningBody.objects.all().order_by('account')
    serializer_class = GoverningBodySerializer
    permission_classes = [IsHeadmasterSafe]
