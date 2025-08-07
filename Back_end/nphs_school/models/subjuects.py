from django.core.exceptions import ValidationError
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=4, unique=True)
    written_marks = models.PositiveIntegerField(default=0)
    practical_marks = models.PositiveIntegerField(default=0)
    mcq_marks = models.PositiveIntegerField(default=0)

    @property
    def total_marks(self):
        return self.written_marks + self.practical_marks + self.mcq_marks

    def clean(self):
        if self.total_marks > 100:
            raise ValidationError("Total marks cannot exceed 100.")

    def __str__(self):
        return f"{self.name} - {self.code}"
