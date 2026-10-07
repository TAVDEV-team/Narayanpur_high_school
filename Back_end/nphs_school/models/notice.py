from datetime import date
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from django.contrib import admin
from django.db import models
from django.utils.text import slugify
from school_backend.logger import get_logger

logger = get_logger(__name__)


class Notice(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()

    # Approval tracking
    approved_by_headmaster = models.BooleanField(
        default=False, editable=False, db_index=True
    )
    approved_at = models.DateTimeField(null=True, blank=True, editable=False)

    # Metadata
    notice_for_date = models.DateField(
        help_text="The date when the notice needs to be published.",
        db_index=True,
        default=date.today,
    )
    slug = models.SlugField(
        max_length=300, unique=True, blank=True, editable=False
    )

    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'notice_for_date'],
                name='unique_notice_per_date',
            )
        ]
        ordering = ['-notice_for_date', '-created_at']
        verbose_name = "Notice"
        verbose_name_plural = "Notices"

    # Short description preview
    @property
    def short_description(self):
        return (
            f"{self.description[:50]}..."
            if len(self.description) > 50
            else self.description
        )

    @short_description.setter
    def short_description(self, value):
        # Prevent accidental writes
        raise AttributeError("short_description is read-only")

    # Admin display
    @admin.display(boolean=True, description="Approved")
    def is_approved(self):
        return self.approved_by_headmaster

    # Business method: approve notice
    # only headmaster can approve

    def approve(self, user):
        from accounts.models import HeadMasterAccount

        if not HeadMasterAccount.is_headmaster(user):
            logger.warning(
                "Unauthorized approval attempt on %s by %s", self.slug, user
            )
            raise PermissionDenied(
                "Only the headmaster can approve this notice."
            )

        if self.approved_by_headmaster:
            logger.warning(
                "Notice %s already approved; ignoring duplicate call by %s",
                self.slug,
                user,
            )
            return False

        self.approved_by_headmaster = True
        self.approved_at = timezone.now()
        self.save(update_fields=["approved_by_headmaster", "approved_at"])
        logger.info("Notice %s approved by %s", self.slug, user)
        return True

    # Slug generation
    def save(self, *args, **kwargs):
        # Assign slug only on creation
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
