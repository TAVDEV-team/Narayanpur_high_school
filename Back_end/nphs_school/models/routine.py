from django.db import models


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

    CLASS_SLOTS = [
        ("1", "10:00 AM - 10:45 AM"),
        ("2", "10:45 AM - 11:30 AM"),
        ("3", "11:30 AM - 12:15 PM"),
        ("4", "12:15 PM - 01:00 PM"),
        ("5", "01:00 PM - 02:00 PM"),
        ("6", "02:00 PM - 02:40 PM"),
        ("7", "02:40 PM - 03:20 PM"),
        ("8", "03:20 PM - 04:00 PM"),
    ]

    aclass = models.ForeignKey(
        "nphs_school.AClass", on_delete=models.CASCADE, related_name="routines"
    )
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    subject = models.ForeignKey(
        "nphs_school.Subject", on_delete=models.SET_NULL, null=True, blank=True
    )
    teacher = models.ForeignKey(
        "accounts.TeacherAccount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    slot = models.CharField(max_length=2, choices=CLASS_SLOTS)

    class Meta:
        ordering = ["aclass", "day", "slot"]
        unique_together = (
            "aclass",
            "day",
            "slot",
        )  # no duplicate routines in same slot

    def __str__(self):
        return f"{self.aclass} - {self.get_day_display()} - {self.get_slot_display()} - {self.subject}"  # noqa: E501
