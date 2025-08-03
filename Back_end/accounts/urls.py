from rest_framework.routers import DefaultRouter
from django.urls import path, include

from accounts.views import (
    StudentAccountViewSet,
    TeacherAccountViewSet,
    HeadMasterAccountViewSet,
    OfficeHelpersAccountViewSet
)

router = DefaultRouter()
router.register(r'students', StudentAccountViewSet, basename='student')
router.register(r'teachers', TeacherAccountViewSet, basename='teacher')
router.register(r'headmaster', HeadMasterAccountViewSet, basename='headmaster')
router.register(r'office-helpers', OfficeHelpersAccountViewSet, basename='office-helper')

urlpatterns = [
    path('', include(router.urls)),
]
