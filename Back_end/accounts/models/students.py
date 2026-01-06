from django.db import models, transaction

from accounts.models import Account
from nphs_school.models import Batch, Subject


class GroupChoices(models.TextChoices):
    SCIENCE = "science", "Science"
    HUMANITIES = "humanities", "Humanities"
    BUSINESS = "business studies", "Business Studies"
    NONE = "none", "No Group"


class StudentAccount(models.Model):

    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="student_profile"
    )
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    roll_number = models.PositiveIntegerField()
    group = models.CharField(
        max_length=20, choices=GroupChoices.choices, default=GroupChoices.NONE
    )

    subjects = models.ManyToManyField(
        Subject, through="StudentSubject", related_name="students"
    )

    class Meta:
        unique_together = ("batch", "roll_number", "group")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk and not self.roll_number:

            with transaction.atomic():
                last_roll = (
                    StudentAccount.objects.select_for_update()
                    .filter(batch=self.batch, group=self.group)
                    .order_by("-roll_number")
                    .first()
                )
                self.roll_number = (
                    (last_roll.roll_number + 1) if last_roll else 1
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.account)


class StudentSubject(models.Model):
    class SubjectType(models.TextChoices):
        COMPULSORY = "compulsory", "Compulsory"
        RELIGIOUS = "religious", "Religious"
        GROUP = "group", "Group"
        OPTIONAL = "optional", "Optional"

    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_type = models.CharField(max_length=20, choices=SubjectType.choices)

    class Meta:
        unique_together = ("student", "subject", "subject_type")

    def __str__(self):
        return f"{self.subject} {self.student}"
