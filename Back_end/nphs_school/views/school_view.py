from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from nphs_school.models import School
from nphs_school.serializers import SchoolSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [AllowAny]
