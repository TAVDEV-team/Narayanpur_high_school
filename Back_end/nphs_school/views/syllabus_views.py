from rest_framework import viewsets

from nphs_school.models import Syllabus
from nphs_school.serializers import SyllabusSerializer


class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
