from rest_framework import viewsets

from accounts.models import GoverningBody
from accounts.serializers import GoverningBodySerializer


class GoverningBodyViewSet(viewsets.ModelViewSet):
    queryset = GoverningBody.objects.all()
    serializer_class = GoverningBodySerializer
