from django.contrib import admin

from .models import (
    Account,
    HeadMasterAccount,
    OfficeHelpersAccount,
    StudentAccount,
    TeacherAccount,
)

admin.site.register(Account)
admin.site.register(StudentAccount)
admin.site.register(TeacherAccount)
admin.site.register(HeadMasterAccount)
admin.site.register(OfficeHelpersAccount)
