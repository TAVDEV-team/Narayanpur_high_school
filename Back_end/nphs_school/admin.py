from django.contrib import admin

from nphs_school.models import (
    About,
    AClass,
    Batch,
    Notice,
    School,
    Subject,
    Routine,
    Syllabus,
)

# class AboutAdmin(admin.ModelAdmin):
#     search_fields = ['name']

# class SchoolAdmin(admin.ModelAdmin):
#     list_filter = ['created_at', 'head_master']
#     search_fields = ['name']

admin.site.register(About)
admin.site.register(School)
admin.site.register(AClass)
admin.site.register(Batch)
admin.site.register(Subject)
admin.site.register(Notice)
admin.site.register(Routine)
admin.site.register(Syllabus)
