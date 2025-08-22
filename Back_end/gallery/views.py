from rest_framework import viewsets

from .models import Photo, PhotoCategory
from .serializers import PhotoCategorySerializer, PhotoSerializer


class PhotoCategoryViewSet(viewsets.ModelViewSet):
    queryset = PhotoCategory.objects.all().order_by("name")
    serializer_class = PhotoCategorySerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by("-date_uploaded")
    serializer_class = PhotoSerializer
