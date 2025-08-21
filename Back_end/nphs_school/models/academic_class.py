from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models

from .subject import Subject

CLASS_CHOICES = [
    ("6", "Class 6"),
    ("7", "Class 7"),
    ("8", "Class 8"),
    ("9_science", "Class 9 Science"),
    ("10_science", "Class 10 Science"),
    ("9_business", "Class 9 Business"),
    ("10_business", "Class 10 Business"),
    ("9_humanities", "Class 9 Humanities"),
    ("10_humanities", "Class 10 Humanities"),
]


class AClass(models.Model):
    name = models.CharField(max_length=20, choices=CLASS_CHOICES, unique=True)
    batch = models.ForeignKey(
        'Batch', on_delete=models.SET_NULL, null=True, blank=True
    )
    compulsory = models.ManyToManyField(
        Subject, related_name="main_classes", blank=True
    )
    group_subjects = models.ManyToManyField(
        Subject, related_name="group_classes", blank=True
    )
    religious = models.ManyToManyField(
        Subject, related_name="religional_classes", blank=True
    )
    extra = models.ManyToManyField(Subject, related_name="extra", blank=True)

    room_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return dict(CLASS_CHOICES).get(self.name, self.name)

    def clean(self):
        if not self.pk:
            return

        errors = {}

        # Check compulsory subjects
        wrong_compulsory = [
            sub.name
            for sub in self.compulsory.all()
            if sub.subject_type != Subject.SubjectType.COMPULSORY
        ]
        if wrong_compulsory:
            errors['compulsory'] = [
                f"{name} is not compulsory" for name in wrong_compulsory
            ]

        # Check group subjects
        wrong_group = [
            sub.name
            for sub in self.group_subjects.all()
            if sub.subject_type
            not in [
                Subject.SubjectType.GROUP,
                Subject.SubjectType.GROUP_OPTIONAL,
            ]
        ]
        if wrong_group:
            errors['group_subjects'] = [
                f"{name} is not a group or group_optional subject"
                for name in wrong_group
            ]

        # Check religious subjects
        wrong_religious = [
            sub.name
            for sub in self.religious.all()
            if sub.subject_type != Subject.SubjectType.RELIGIOUS
        ]
        if wrong_religious:
            errors['religious'] = [
                f"{name} is not religious" for name in wrong_religious
            ]

        # Check extra subjects
        wrong_extra = [
            sub.name
            for sub in self.extra.all()
            if sub.subject_type != Subject.SubjectType.EXTRA
        ]
        if wrong_extra:
            errors['extra'] = [f"{name} is not extra" for name in wrong_extra]

        # Raise all collected errors at once
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def students(self):
        StudentAccount = apps.get_model("accounts", "StudentAccount")
        return StudentAccount.objects.filter(batch__current_class=self)
