from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.views import ExamViewSet, ResultViewSet
from .views.class_fast_result import ClassFastResultAPIView

router = DefaultRouter()
router.register(r"exam", ExamViewSet, basename="exam")
router.register(r"", ResultViewSet, basename="result")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "class_fast/<int:class_id>/<int:exam_id>/",
        ClassFastResultAPIView.as_view(),
        name="class_fast_result"
    ),
]
