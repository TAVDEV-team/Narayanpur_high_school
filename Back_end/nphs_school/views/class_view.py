from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import (
    StudentListSerializer,
    StudentMinListSerializer,
)
from nphs_school.models import AClass
from nphs_school.serializers import AClassMetaSerializer, AClassSerializer

from rest_framework import status
from rest_framework.exceptions import ValidationError


class StudentPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 100


@method_decorator(cache_page(60 * 60 * 12), name="list")
@method_decorator(cache_page(60 * 60 * 12), name="retrieve")
class AClassViewSet(viewsets.ModelViewSet):
    queryset = AClass.objects.all().order_by("grade")
    serializer_class = AClassSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return AClassMetaSerializer
        return AClassSerializer

    @action(detail=True, methods=["get"], url_path="students")
    @method_decorator(cache_page(60 * 60))
    def students(self, request, pk=None):

        aclass = self.get_object()

        qs = (
            aclass.students().select_related("account").order_by("roll_number")
        )

        paginator = StudentPagination()
        page = paginator.paginate_queryset(qs, request)

        serializer = StudentListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=["get"], url_path="students/lookup")
    def student_lookup(self, request, pk=None):
        aclass = self.get_object()

        roll_number = request.query_params.get("roll_number")

        # 1. Validate input
        if roll_number is None:
            raise ValidationError(
                {"roll_number": "This query parameter is required."}
            )

        try:
            roll_number = int(roll_number)
        except ValueError:
            raise ValidationError({"roll_number": "Must be an integer."})

        # 2. Query
        qs = (
            aclass.students()
            .select_related("account")
            .filter(roll_number=roll_number)
        )

        # 3. Integrity check
        if qs.count() > 1:
            return Response(
                {"detail": "Data integrity error: duplicate roll numbers."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 4. Serialize
        serializer = StudentMinListSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    @method_decorator(cache_page(60 * 60 * 12))
    def meta(self, request, pk=None):
        instance = self.get_object()
        serializer = AClassMetaSerializer(instance)
        return Response(serializer.data)
