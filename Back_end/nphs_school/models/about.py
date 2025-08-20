from datetime import date

from django.db import models
from solo.models import SingletonModel


class About(SingletonModel):
    """
    Singleton model storing institutional metadata and static CMS content.

    Fields:
        - name (CharField): Official institution name (non-editable).
        - established_at (DateField): Founding date of the institution.
        - eiin : Official EIIN number assigned by the education board.
        - location_url (URLField): Google Maps or physical map URL.
        - location_address (CharField): Street/area-level physical address.
        - history (TextField): A narrative description of the school's history.
        - motto (CharField): School tagline or mission (optional).
        - logo (ImageField): Main logo used for branding (optional).
        - favicon (ImageField): Favicon image for the frontend (optional).
        - social_links (JSONField): Dict of platform →\
            link (e.g., {"facebook": "url"}).
        - extra : Arbitrary config space (e.g., contact emails, themes).
        - created_at (DateTimeField): Timestamp when the record was created.
        - updated_at : Auto-updated on changes.
    Methods:
        __str__: Returns the name for admin and console representation.
    Notes:
        - Only one instance is allowed (enforced by `solo` package).
        - Designed to power frontend CMS sections.
    """

    name = models.CharField(
        max_length=200,
        default=" High School",
    )
    eiin = models.CharField(max_length=7, default="105000")
    established_at = models.DateField(default=date(1980, 1, 1))
    location_url = models.URLField(
        default="https://maps.app.goo.gl/YSq6eubdtMss756a8"
    )
    location_address = models.CharField(
        default="Narayan pur, Amjad-Nagar, Chauddagram-3500", max_length=255
    )
    history = models.TextField()
    motto = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to="branding/", null=True, blank=True)
    favicon = models.ImageField(upload_to="branding/", null=True, blank=True)
    social_links = models.JSONField(default=dict, blank=True, null=True)
    extra = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Institution Profile"
        verbose_name_plural = "Institution Profile"
