from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from accounts.views import (
    AccountViewSet,
    ChangePasswordView,
    GoverningBodyViewSet,
    HeadMasterAccountViewSet,
    LogoutView,
    OfficeHelpersAccountViewSet,
    StudentAccountViewSet,
    TeacherAccountViewSet,
    CustomTokenObtainPairView,
)

router = DefaultRouter()
router.register(r"account", AccountViewSet, basename="account")
router.register(r"students", StudentAccountViewSet, basename="student")
router.register(r"teachers", TeacherAccountViewSet, basename="teacher")
router.register(r"headmaster", HeadMasterAccountViewSet, basename="headmaster")
router.register(r"governing", GoverningBodyViewSet, basename="governing")
router.register(
    r"office-helpers", OfficeHelpersAccountViewSet, basename="office-helper"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
