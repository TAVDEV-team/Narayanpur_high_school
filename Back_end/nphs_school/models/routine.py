from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import TeacherAccount
from nphs_school.models import AClass, Subject


class Routine(models.Model):
    DAYS_OF_WEEK = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
        ("SUN", "Sunday"),
    ]

    aclass = models.ForeignKey(
        AClass, on_delete=models.CASCADE, related_name="routines"
    )
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, blank=True
    )
    teacher = models.ForeignKey(
        TeacherAccount, on_delete=models.SET_NULL, null=True, blank=True
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["aclass", "day", "start_time"]

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

    def __str__(self):
        return f"{self.aclass} - {self.get_day_display()} - {self.subject}"
