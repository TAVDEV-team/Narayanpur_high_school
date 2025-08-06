from django.contrib import admin
from nphs_school.models import About, AClass, Batch, School, Subjects

# class AboutAdmin(admin.ModelAdmin):
#     search_fields = ['name']

# class SchoolAdmin(admin.ModelAdmin):
#     list_filter = ['created_at', 'head_master']
#     search_fields = ['name']

admin.site.register(About)
admin.site.register(School)
admin.site.register(AClass)
admin.site.register(Batch)
admin.site.register(Subjects)
