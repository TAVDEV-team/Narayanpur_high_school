from rest_framework import viewsets

from nphs_school.models import Batch
from nphs_school.serializers import BatchSerializer


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
