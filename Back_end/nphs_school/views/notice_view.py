from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsHeadMaster
from nphs_school.models import Notice
from nphs_school.serializers import NoticeSerializer


@method_decorator(cache_page(60 * 5), name="list")
@method_decorator(cache_page(60 * 5), name="retrieve")
class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]

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
        permission_classes=[AllowAny]
        # permission_classes=[IsTeacher],
    )
    @method_decorator(cache_page(60 * 5))
    def pending_list(self, request):
        pending = Notice.objects.filter(
            approved_by_headmaster=False, is_active=True
        ).order_by("-created_at")
        return self._paginate_and_respond(pending)

    def perform_create(self, serializer):
        cache.delete_pattern("views.decorators.cache*")

    @action(
        detail=True,
        url_path="approve",
        permission_classes=[IsAuthenticated, IsHeadMaster],
    )
    @method_decorator(cache_page(60 * 5))
    def approve_notice(self, request, pk=None):
        notice = self.get_object()
        notice.approve(request.user)
        return Response({"detail": "Notice approved successfully."})

    def _paginate_and_respond(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
