from django.db import models
from solo.models import SingletonModel


class School(SingletonModel):
    """
    Central configuration for the entire school entity.

    Fields:
        - name: Official name of the school.
        - code: Internal school identifier (e.g., NHS001).
        - head_master: Primary administrator (principal).
        - motto: School's mission or branding tagline.
        - logo: Official logo for branding.
        - location_address: Physical address of the school.
        - contact_email: General contact email (optional).
        - contact_phone: Public phone number (optional).
        - created_at: Timestamp of record creation.
        - updated_at: Timestamp of last update.

    Methods:
        __str__: Returns school name and code for clarity in admin/UIs.

    Notes:
        - Enforced singleton via `django-solo`.
        - Intended to serve as central anchor across all school-related apps.
    """

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, default="105409", unique=True)
    motto = models.CharField(max_length=120, blank=True)
    logo = models.ImageField(upload_to="schools/", null=True, blank=True)
    location_address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
