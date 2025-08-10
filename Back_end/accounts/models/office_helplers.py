from django.db import models

from accounts.models import Account


class OfficeHelpersAccount(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="office_roles"
    )
    designation = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.account.full_name} - {self.designation}"

    class Meta:
        unique_together = ("account", "designation")
