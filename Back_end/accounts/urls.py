from rest_framework.routers import DefaultRouter
from django.urls import path, include

from accounts.views import (
    StudentAccountViewSet,
    TeacherAccountViewSet,
    HeadMasterAccountViewSet,
    OfficeHelpersAccountViewSet
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'students', StudentAccountViewSet, basename='student')
router.register(r'teachers', TeacherAccountViewSet, basename='teacher')
router.register(r'headmaster', HeadMasterAccountViewSet, basename='headmaster')
router.register(r'office-helpers', OfficeHelpersAccountViewSet, basename='office-helper')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
