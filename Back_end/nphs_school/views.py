from django.shortcuts import render

from nphs_school.serializers import AboutSerializer, SchoolSerializer, BatchSerializer, AClassSerializer
from nphs_school.models import About, School, AClass, Batch

from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import viewsets, status

class AboutViewSet(viewsets.ViewSet):
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



class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class AClassViewSet(viewsets.ModelViewSet):
    queryset = AClass.objects.all()
    serializer_class = AClassSerializer


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
