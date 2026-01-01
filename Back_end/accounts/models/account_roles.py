from django.db import models


class AccountRole(models.TextChoices):
    STUDENT = "student", "Student"
    TEACHER = "teacher", "Teacher"
    HEADMASTER = "headmaster", "Headmaster"
    OFFICE_STAFF = "office_staff", "Office Staff"
