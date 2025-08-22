from django.contrib import admin

# Register your models here.
from .models import Photo, PhotoCategory

admin.site.register(PhotoCategory)
admin.site.register(Photo)
