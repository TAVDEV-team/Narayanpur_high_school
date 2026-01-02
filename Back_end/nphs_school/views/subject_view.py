from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from nphs_school.models import Subject
from nphs_school.serializers import SubjectSerializer, SubjectListSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return SubjectListSerializer
        return SubjectSerializer
