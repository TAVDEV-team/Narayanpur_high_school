from django.db import models


class Exam(models.Model):
    exam_title = models.CharField(
        max_length=50,
        choices=[
            ('midterm', 'Midterm'),
            ('final', 'Final'),
            ('test', 'Test'),
        ],
    )
    starting_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.exam_title = f"{self.exam_title} {self.starting_date.year}"
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.exam_title}"
