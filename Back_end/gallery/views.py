from rest_framework import viewsets

from accounts.permissions import ReadOnlyOrRestricted
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Photo, PhotoCategory
from .serializers import PhotoCategorySerializer, PhotoSerializer


@method_decorator(cache_page(60 * 5), name="list")  # cache list view 5 mins
@method_decorator(
    cache_page(60 * 5), name="retrieve"
)  # cache detail view 5 mins
class PhotoCategoryViewSet(viewsets.ModelViewSet):
    queryset = PhotoCategory.objects.all().order_by("name")
    serializer_class = PhotoCategorySerializer
    permission_classes = [ReadOnlyOrRestricted]


@method_decorator(cache_page(60 * 5), name="list")  # cache list view 5 mins
@method_decorator(
    cache_page(60 * 5), name="retrieve"
)  # cache detail view 5 mins
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by("-date_uploaded")
    serializer_class = PhotoSerializer
    permission_classes = [ReadOnlyOrRestricted]
