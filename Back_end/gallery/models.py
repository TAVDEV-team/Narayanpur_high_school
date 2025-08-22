from django.db import models
from django.utils import timezone


class PhotoCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Photo Categories"

    def __str__(self):
        return self.name


class Photo(models.Model):
    category = models.ForeignKey(
        PhotoCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="photos",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="gallery/")
    date_uploaded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
