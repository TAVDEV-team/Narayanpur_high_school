from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ResultViewSet, ExamViewSet

router = DefaultRouter()
router.register(r"", ResultViewSet, basename="result")
router.register(r"exam", ExamViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
