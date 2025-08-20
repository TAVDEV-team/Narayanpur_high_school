from django.db import models

from accounts.models import Account, HeadMasterAccount


class GoverningBody(models.Model):
    class Designations(models.TextChoices):
        SECRETARY = "secretary", "Secretary"
        MEMBER_SECRETARY = "member_secretary", "Member Secretary"
        MEMBER = "member", "Member"

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Used for all designations except Member Secretary",
    )
    head_master = models.OneToOneField(
        HeadMasterAccount,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Only for Member Secretary",
    )
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
            if self.head_master is None:
                raise ValidationError(
                    "Member Secretary must be the Headmaster."
                )
            if self.account is not None:
                raise ValidationError(
                    "Member Secretary cannot have a regular Account."
                )

        # Members can’t be HeadMaster
        if self.designation == self.Designations.MEMBER:
            if self.head_master is not None:
                raise ValidationError("Members cannot be Headmaster.")

    def __str__(self):
        if self.designation == self.Designations.MEMBER_SECRETARY:
            return f"{self.designation} - {self.head_master}"
        return f"{self.designation} - {self.account}"
