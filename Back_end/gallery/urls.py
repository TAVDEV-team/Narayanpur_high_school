from rest_framework.routers import DefaultRouter

from .views import PhotoCategoryViewSet, PhotoViewSet

router = DefaultRouter()
router.register(r'categories', PhotoCategoryViewSet)
router.register(r'photos', PhotoViewSet)

urlpatterns = router.urls
