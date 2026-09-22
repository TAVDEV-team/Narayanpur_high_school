from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsHeadMaster, IsTeacher
from nphs_school.models import Notice
from nphs_school.serializers import NoticeSerializer
from school_backend.logger import get_logger

logger = get_logger(__name__)


@method_decorator(cache_page(60 * 5), name="list")
@method_decorator(cache_page(60 * 5), name="retrieve")
class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["get"],
        url_path="approved",
        permission_classes=[AllowAny],
    )
    @method_decorator(cache_page(60 * 5))
    def approved_list(self, request):
        notices = Notice.objects.filter(
            approved_by_headmaster=True, is_active=True
        ).order_by("-notice_for_date", "-created_at")
        logger.debug(
            "approved_list requested by %s (%d results)",
            request.user if request.user.is_authenticated else "anonymous",
            notices.count(),
        )
        return self._paginate_and_respond(notices)

    @action(
        detail=False,
        methods=["get"],
        url_path="pending",
        permission_classes=[IsTeacher | IsHeadMaster],
    )
    def pending_list(self, request):
        pending = Notice.objects.filter(
            approved_by_headmaster=False, is_active=True
        ).order_by("-notice_for_date", "-created_at")
        logger.info(
            "pending_list requested by %s (%d results)",
            request.user,
            pending.count(),
        )
        return self._paginate_and_respond(pending)

    @action(detail=True, url_path="approve", permission_classes=[IsHeadMaster])
    def approve_notice(self, request, pk=None):
        notice = self.get_object()
        logger.info(
            "approve_notice called: notice=%s (id=%s) by user=%s",
            notice.slug,
            notice.pk,
            request.user,
        )
        try:
            approved = notice.approve(request.user)
        except PermissionDenied as exc:
            logger.warning(
                "approve_notice denied: notice=%s by user=%s reason=%s",
                notice.slug,
                request.user,
                exc,
            )
            return Response(
                {"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN
            )

        if not approved:
            logger.info(
                "approve_notice no-op: notice=%s\
                already approved (requested by %s)",
                notice.slug,
                request.user,
            )
            return Response(
                {"detail": "Notice was already approved."},
                status=status.HTTP_200_OK,
            )

        logger.info(
            "approve_notice succeeded: notice=%s by user=%s",
            notice.slug,
            request.user,
        )
        return Response({"detail": "Notice approved successfully."})

    def perform_create(self, serializer):
        notice = serializer.save()
        logger.info(
            "Notice created: %s (id=%s) by user=%s",
            notice.slug,
            notice.pk,
            self.request.user,
        )

    def perform_update(self, serializer):
        notice = serializer.save()
        logger.info(
            "Notice updated: %s (id=%s) by user=%s",
            notice.slug,
            notice.pk,
            self.request.user,
        )

    def perform_destroy(self, instance):
        logger.warning(
            "Notice deleted: %s (id=%s) by user=%s",
            instance.slug,
            instance.pk,
            self.request.user,
        )
        instance.delete()

    def _paginate_and_respond(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
