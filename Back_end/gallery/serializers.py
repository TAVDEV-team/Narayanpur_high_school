from rest_framework import serializers

from .models import Photo, PhotoCategory


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [
            "id",
            "title",
            "category",
            "description",
            "image",
            "date_uploaded",
        ]


class PhotoCategorySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = PhotoCategory
        fields = ["id", "name", "description", "photos"]
