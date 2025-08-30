from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from accounts.models import GoverningBody
from accounts.serializers import GoverningBodySerializer


class GoverningBodyViewSet(viewsets.ModelViewSet):
    queryset = GoverningBody.objects.all()
    serializer_class = GoverningBodySerializer
    permission_classes = [AllowAny]
