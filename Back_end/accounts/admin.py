from django.contrib import admin
from .models import (
    Account, 
    StudentAccount, 
    TeacherAccount, 
    OfficeHelpersAccount,
    HeadMasterAccount, 
    )


admin.site.register(Account)
admin.site.register(StudentAccount)
admin.site.register(TeacherAccount)
admin.site.register(HeadMasterAccount)
admin.site.register(OfficeHelpersAccount)
