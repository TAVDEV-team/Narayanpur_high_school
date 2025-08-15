from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import StudentAccount
from accounts.permissions import IsHeadMaster, IsTeacher
from accounts.serializers import StudentSerializer
from nphs_school.models import About, AClass, Batch, Notice, School, Subject
from nphs_school.serializers import (
    AboutSerializer,
    AClassSerializer,
    BatchSerializer,
    NoticeSerializer,
    SchoolSerializer,
    SubjectSerializer,
)


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

    @action(detail=True, methods=["get"], url_path="detail")
    def get_detail(self, request, pk=None):
        aclass = self.get_object()
        students = StudentAccount.objects.filter(batch__current_class=aclass)
        student_serializer = StudentSerializer(students, many=True)

        return Response(
            {
                "aclass": self.get_serializer(aclass).data,
                "students": student_serializer.data,
            }
        )


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="approved",
        permission_classes=[AllowAny],
    )
    def approved_list(self, request):
        notices = Notice.objects.filter(
            approved_by_headmaster=True, is_active=True
        ).order_by("-notice_for_date", "-created_at")
        return self._paginate_and_respond(notices)

    @action(
        detail=False,
        methods=["get"],
        url_path="pending",
        permission_classes=[IsTeacher],
    )
    def pending_list(self, request):
        pending = Notice.objects.filter(
            approved_by_headmaster=False, is_active=True
        ).order_by("-created_at")
        return self._paginate_and_respond(pending)

    def perform_create(self, serializer):
        serializer.save(written_by=self.request.user)

    @action(
        detail=True,
        url_path="approve",
        permission_classes=[IsAuthenticated, IsHeadMaster],
    )
    def approve_notice(self, request, pk=None):
        notice = self.get_object()  # DRF automatically uses pk from URL
        notice.approve(request.user)
        return Response({"detail": "Notice approved successfully."})

    def _paginate_and_respond(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
