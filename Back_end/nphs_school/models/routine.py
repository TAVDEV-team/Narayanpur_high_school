from django.db import models
from django.core.exceptions import ValidationError
from school_backend.logger import get_logger

logger = get_logger(__name__)


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
        constraints = [
            models.UniqueConstraint(
                fields=["aclass", "day", "slot"], name="unique_class_day_slot"
            ),
            models.UniqueConstraint(
                fields=["teacher", "day", "slot"],
                name="unique_teacher_day_slot",
            ),
        ]

    def __str__(self):
        return f"{self.aclass} - {self.get_day_display()} - {self.get_slot_display()} - {self.subject}"  # noqa: E501

    def clean(self):
        conflict_qs = Routine.objects.filter(
            day=self.day, slot=self.slot
        ).exclude(pk=self.pk)
        class_conflict = conflict_qs.filter(aclass=self.aclass).first()
        if class_conflict:
            logger.warning(
                "Routine conflict: class\
                    %s already booked %s slot %s (existing subject=%s)",
                self.aclass,
                self.day,
                self.slot,
                class_conflict.subject,
            )
            raise ValidationError(
                f"{self.aclass} already has a class \
                    scheduled for {self.get_day_display()} "
                f"slot {self.slot}."
            )

        if self.teacher_id:
            teacher_conflict = conflict_qs.filter(teacher=self.teacher).first()
            if teacher_conflict:
                logger.warning(
                    "Routine conflict: teacher %s \
                        already booked %s slot %s (existing class=%s)",
                    self.teacher,
                    self.day,
                    self.slot,
                    teacher_conflict.aclass,
                )
                raise ValidationError(
                    f"{self.teacher} is already scheduled elsewhere on "
                    f"{self.get_day_display()} slot {self.slot}."
                )

    def save(self, *args, **kwargs):
        if self.pk:
            old = Routine.objects.filter(pk=self.pk).first()
            if old and old.teacher_id != self.teacher_id:
                logger.info(
                    "Routine %s reassigned: teacher %s -> %s (%s slot %s)",
                    self.pk,
                    old.teacher,
                    self.teacher,
                    self.day,
                    self.slot,
                )
            if old and old.subject_id != self.subject_id:
                logger.info(
                    "Routine %s subject changed: %s -> %s (%s slot %s)",
                    self.pk,
                    old.subject,
                    self.subject,
                    self.day,
                    self.slot,
                )
        self.full_clean()  # triggers clean() above
        super().save(*args, **kwargs)
