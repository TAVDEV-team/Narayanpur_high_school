from rest_framework import viewsets

from nphs_school.models import School
from nphs_school.serializers import SchoolSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
