from accounts.models import Account
from django.db import models, transaction
from nphs_school.models import Batch

GROUP_CHOICES = [
    (grp, grp.title()) for grp in ["science", "humanities", "business studies"]
]


class StudentAccount(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="student_profile"
    )
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    roll_number = models.PositiveIntegerField(editable=False)
    group = models.CharField(
        max_length=20, choices=GROUP_CHOICES, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.pk and not self.roll_number:
            with transaction.atomic():
                last_roll = (
                    StudentAccount.objects.select_for_update()
                    .filter(batch=self.batch)
                    .order_by("-roll_number")
                    .first()
                )
                self.roll_number = (
                    (last_roll.roll_number + 1) if last_roll else 1
                )
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("batch", "roll_number")
