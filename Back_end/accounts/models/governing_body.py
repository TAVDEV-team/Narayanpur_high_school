from django.db import models

from accounts.models import Account

from .teacher import HeadMasterAccount


class GoverningBody(models.Model):
    class Designations(models.TextChoices):
        SECRETARY = "secretary", "Secretary"
        MEMBER_SECRETARY = "member_secretary", "Member Secretary"
        MEMBER = "member", "Member"

    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, default=1
    )
    profession = models.CharField(max_length=100, default='Teacher')
    designation = models.CharField(max_length=30, choices=Designations.choices)

    def clean(self):
        from django.core.exceptions import ValidationError

        # only 1 Secretary
        if self.designation == self.Designations.SECRETARY:
            if (
                GoverningBody.objects.filter(
                    designation=self.Designations.SECRETARY
                )
                .exclude(pk=self.pk)
                .exists()
            ):
                raise ValidationError("Only one Secretary allowed.")

        # only 1 Member Secretary and must be HeadMaster
        if self.designation == self.Designations.MEMBER_SECRETARY:
            if (
                GoverningBody.objects.filter(
                    designation=self.Designations.MEMBER_SECRETARY
                )
                .exclude(pk=self.pk)
                .exists()
            ):
                raise ValidationError("Only one Member Secretary allowed.")
            if (
                HeadMasterAccount.objects.filter(account__account=self.account)
            ) is None:
                raise ValidationError(
                    "Member Secretary must be the Headmaster."
                )

    def __str__(self):
        return f"{self.designation} - {self.account}"
