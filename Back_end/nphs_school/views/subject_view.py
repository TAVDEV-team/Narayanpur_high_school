from rest_framework import viewsets

from nphs_school.models import Subject
from nphs_school.serializers import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
