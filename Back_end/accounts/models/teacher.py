from django.core.exceptions import ValidationError
from django.db import models
from solo.models import SingletonModel

from accounts.models import Account
from nphs_school.models import AClass, Subject


class TeacherAccount(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="teacher_profile"
    )
    base_subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=1,
    )
    is_class_teacher = models.BooleanField(default=False)
    class_teacher_of = models.ForeignKey(
        AClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="class_teacher",
    )

    def __str__(self):
        subject = self.base_subject if self.base_subject else "No Subject"
        return f"{self.account.full_name} - {subject}"

    def clean(self):
        if self.is_class_teacher and not self.class_teacher_of:
            raise ValidationError("Class teacher must be assigned to a class.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class HeadMasterAccount(SingletonModel):
    teacher = models.ForeignKey(
        TeacherAccount,
        on_delete=models.CASCADE,
        related_name="headmaster_profile",
    )
    appointed_date = models.DateField()

    def __str__(self):
        return (
            f"Headmaster: {self.teacher.account.full_name}"
            if self.teacher
            else "Unassigned Headmaster"
        )
