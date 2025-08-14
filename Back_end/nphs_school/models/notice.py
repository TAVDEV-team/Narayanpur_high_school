from datetime import date

from django.db import models
from django.utils.text import slugify


class Notice(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    approved_by_headmaster = models.BooleanField(
        default=False,
        db_index=True,
        # editable=False
    )
    notice_for_date = models.DateField(
        help_text="The date when the notice needs to be published.",
        db_index=True,
        default=date.today
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        blank=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'notice_for_date'],
                name='unique_notice_per_date'
                )
        ]
        ordering = ['-notice_for_date', '-created_at']
        verbose_name = "Notice"
        verbose_name_plural = "Notices"

    def short_description(self):
        return (
            self.description[:50] +
            "..." if len(self.description) >
            50 else self.description
            )
    short_description.short_description = "Preview"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:280]
            slug_candidate = base_slug
            counter = 1
            while Notice.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.notice_for_date})"
