from django.urls import include, path
from rest_framework.routers import DefaultRouter

from nphs_school.views import (
    AboutViewSet,
    AClassViewSet,
    BatchViewSet,
    NoticeViewSet,
    SchoolViewSet,
    SubjectViewSet,
    RoutineViewSet,
)

router = DefaultRouter()


router.register(r"schools", SchoolViewSet)
router.register(r"classes", AClassViewSet)
router.register(r"batches", BatchViewSet)
router.register(r"notices", NoticeViewSet)
router.register(r"Subject", SubjectViewSet)
router.register(r"routine", RoutineViewSet)

about_list = AboutViewSet.as_view(
    {
        "get": "list",
        "patch": "update",
        "put": "update",
    }
)

urlpatterns = [
    path("about/", about_list, name="about-singleton"),
    path("", include(router.urls)),
]
