from django.http import FileResponse, Http404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from nphs_school.models import Syllabus
from nphs_school.serializers import SyllabusSerializer


class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        try:
            syllabus = self.get_object()
            return FileResponse(
                syllabus.file.open("rb"),
                as_attachment=True,
                filename=syllabus.file.name.split("/")[-1],
            )
        except FileNotFoundError:
            raise Http404("File not found.")
