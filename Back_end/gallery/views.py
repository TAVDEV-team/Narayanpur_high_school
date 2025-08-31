from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Photo, PhotoCategory
from .serializers import PhotoCategorySerializer, PhotoSerializer


class PhotoCategoryViewSet(viewsets.ModelViewSet):
    queryset = PhotoCategory.objects.all().order_by("name")
    serializer_class = PhotoCategorySerializer
    permission_classes = [AllowAny]


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by("-date_uploaded")
    serializer_class = PhotoSerializer
    permission_classes = [AllowAny]
