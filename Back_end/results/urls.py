from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExamViewSet, ResultViewSet

router = DefaultRouter()
router.register(r"exam", ExamViewSet, basename="exam")
router.register(r"", ResultViewSet, basename="result")

urlpatterns = [
    path("", include(router.urls)),
]
