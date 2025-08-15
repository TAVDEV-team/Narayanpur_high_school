from rest_framework import status, viewsets
from rest_framework.response import Response

from nphs_school.models import About
from nphs_school.serializers import AboutSerializer


class AboutViewSet(viewsets.ModelViewSet):
    serializer_class = AboutSerializer
    queryset = About.objects.all()

    def list(self, request):
        about = About.get_solo()
        serializer = AboutSerializer(about)
        return Response(serializer.data)

    def update(self, request):
        about = About.get_solo()
        serializer = AboutSerializer(about, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
