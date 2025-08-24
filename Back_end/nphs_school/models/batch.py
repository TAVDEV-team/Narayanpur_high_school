from datetime import date

from django.db import models


class Batch(models.Model):
    """
    Represents a graduating cohort tied to a specific class level.

    Fields:
        label (CharField): Unique batch identifier (e.g., 'ssc2025').
        class_ (ForeignKey): Optional link to the associated SClass.
        graduation year : when they were/are graduated
        created_at (DateTimeField): Timestamp of record creation.
        updated_at (DateTimeField): Auto timestamp of updates.

    Notes:
        - Use label for graduation tracking (e.g., promotion history).
        - `class_` may be null for alumni or archived batches.
    """

    def default_graduation_year():
        return str(date.today().year + 5)

    label = models.CharField(max_length=20, unique=True, editable=False)
    is_graduated = models.BooleanField(
        default=False, help_text="Mark this batch as graduated or archived."
    )
    graduation_year = models.CharField(
        max_length=4,
        choices=[(str(y), str(y)) for y in range(1980, 2055)],
        default=default_graduation_year,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def active_batches(cls):
        return cls.objects.filter(is_graduated=False)

    @property
    def current_class(self):
        from nphs_school.models import AClass

        return AClass.objects.filter(batch=self).first()

    @classmethod
    def archived_batches(cls):
        return cls.objects.filter(is_graduated=True)

    def save(self, *args, **kwargs):
        self.label = f"SSC-{self.graduation_year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label
