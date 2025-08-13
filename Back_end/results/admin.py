from django.contrib import admin

from .models import Exam, Result

# Register your models here.
admin.site.register(Result)
admin.site.register(Exam)
