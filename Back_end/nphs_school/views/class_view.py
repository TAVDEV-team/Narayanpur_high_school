from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
# from
# @method_decorator(cache_page(60 * 5), name="list")
# @method_decorator(cache_page(60 * 5), name="retrieve")
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from nphs_school.models import AClass
from nphs_school.serializers import AClassMetaSerializer, AClassSerializer


class AClassViewSet(viewsets.ModelViewSet):
    queryset = AClass.objects.all()
    serializer_class = AClassSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            AClass.objects.select_related("batch")
            .prefetch_related(
                "compulsory",
                "group_subjects",
                "religious",
                "extra",
            )
            .annotate(
                total_students=Count(
                    "batch__studentaccount",
                    distinct=True,
                ),
                male_students=Count(
                    "batch__studentaccount",
                    filter=Q(batch__studentaccount__account__gender="male"),
                    distinct=True,
                ),
                female_students=Count(
                    "batch__studentaccount",
                    filter=Q(batch__studentaccount__account__gender="female"),
                    distinct=True,
                ),
            )
        )

    @action(detail=True, methods=["get"])
    @method_decorator(cache_page(60 * 5))
    def meta(self, request, pk=None):
        instance = self.get_object()
        serializer = AClassMetaSerializer(instance)
        return Response(serializer.data)
