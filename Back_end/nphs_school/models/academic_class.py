from django.db import models

from .subjects import Subject

CLASS_CHOICES = [(str(i), f"Class {i}") for i in range(6, 11)]


class AClass(models.Model):
    """
    Represents an academic class unit (e.g., Class 6, SSC2025 batch).

    Fields:
        name (CharField): Human-readable class name (e.g., '6', '10 Science').
        room_number : Where the class helds on
        created_at (DateTimeField): Timestamp of creation.
        updated_at (DateTimeField): Auto-updated on change.

    Methods:
        __str__: Returns a readable label\
         for admin/lists (e.g., "Class 10 - Mr. Karim").

    Notes:
        - `total_students` can be manually synced or auto-counted via relation.
    """

    name = models.CharField(max_length=12, choices=CLASS_CHOICES, unique=True)
    Subject = models.ManyToManyField(Subject)
    room_number = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Class {self.name} "
