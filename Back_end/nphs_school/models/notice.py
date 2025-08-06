from django.db import models


class Notice(models.Model):
    title = models.CharField(
        max_length=1000,
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by_headmaster = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.created_at} {self.title}"
