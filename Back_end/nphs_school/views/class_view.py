from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import StudentListSerializer
from nphs_school.models import AClass
from nphs_school.serializers import AClassMetaSerializer, AClassSerializer


class StudentPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 100


class AClassViewSet(viewsets.ModelViewSet):
    queryset = AClass.objects.all().order_by("grade")
    serializer_class = AClassSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return AClassMetaSerializer
        return AClassSerializer

    @action(detail=True, methods=["get"], url_path="students")
    def students(self, request, pk=None):

        aclass = self.get_object()

        qs = (
            aclass.students().select_related("account").order_by("roll_number")
        )

        paginator = StudentPagination()
        page = paginator.paginate_queryset(qs, request)

        serializer = StudentListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=["get"])
    @method_decorator(cache_page(60 * 5))
    def meta(self, request, pk=None):
        instance = self.get_object()
        serializer = AClassMetaSerializer(instance)
        return Response(serializer.data)
