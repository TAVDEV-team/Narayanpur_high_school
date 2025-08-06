from django.urls import include, path
from nphs_school.views import (
    AboutViewSet,
    AClassViewSet,
    BatchViewSet,
    NoticeViewSet,
    SchoolViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register(r"schools", SchoolViewSet)
router.register(r"classes", AClassViewSet)
router.register(r"batches", BatchViewSet)
router.register(r"notices", NoticeViewSet)

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
