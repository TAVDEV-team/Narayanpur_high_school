from nphs_school.models import About, AClass, Batch, Notice, School, Subject
from nphs_school.serializers import (AboutSerializer, AClassSerializer,
                                     BatchSerializer, NoticeSerializer,
                                     SchoolSerializer, Subjecterializer)

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


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


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class AClassViewSet(viewsets.ModelViewSet):
    queryset = AClass.objects.all()
    serializer_class = AClassSerializer


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path=r"approved/",
    )
    def approved_list(self, request):
        notice = Notice.objects.filter(approved_by_headmaster=True)
        serializer = NoticeSerializer(notice, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = Subjecterializer
