import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

RELIGION_CHOICES = [
    (rel, rel.title()) for rel in ["islam", "hindu", "buddhist", "christian"]
]


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(
        max_length=1000, editable=False, default="missing"
    )
    mobile = models.CharField(max_length=14)
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to="Accounts/", null=True, blank=True)
    religion = models.CharField(
        max_length=10, choices=RELIGION_CHOICES, default="islam"
    )
    joining_date = models.DateField(help_text="when he/she joined the school")
    address = models.TextField()
    last_educational_institute = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.user.username}"

    def clean(self):
        normalized = self.normalize_mobile(self.mobile)
        if not re.fullmatch(r"8801[3-9]\d{8}", normalized):
            raise ValidationError(
                {"mobile": "Invalid BD mobile after normalization."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        self.mobile = self.normalize_mobile(self.mobile)
        self.full_name = self.build_full_name()
        super().save(*args, **kwargs)

    def build_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @staticmethod
    def normalize_mobile(raw):
        raw = re.sub(r"\D", "", raw)
        if raw.startswith("8801") and len(raw) == 13:
            return raw
        elif raw.startswith("01") and len(raw) == 11:
            return "88" + raw
        elif raw.startswith("1") and len(raw) == 10:
            return "880" + raw
        raise ValidationError("Invalid Bangladeshi mobile format.")
