from accounts.models import StudentAccount
from django.core.exceptions import ValidationError
from django.db import models
from nphs_school.models import AClass, Subject

from .result_manager import ResultManager


class Result(models.Model):
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    aclass = models.ForeignKey(AClass, on_delete=models.CASCADE, default=1)

    exam_type = models.CharField(
        max_length=10,
        choices=[
            ('midterm', 'Midterm'),
            ('final', 'Final'),
            ('test', 'Test'),
        ],
    )

    objects = ResultManager()
    mcq = models.PositiveIntegerField(default=0)
    practical = models.PositiveIntegerField(default=0)
    writing = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_marks(self):
        return self.mcq + self.practical + self.writing

    @property
    def total_possible(self):
        return self.subject.total_marks

    @property
    def percentage(self):
        return (
            (self.total_marks / float(self.total_possible)) * 100
            if self.total_possible
            else 0
        )

    @property
    def grade(self):
        pct = self.percentage
        grades = [
            (80, 'A+'),
            (70, 'A'),
            (60, 'A-'),
            (50, 'B'),
            (40, 'C'),
            (33, 'D'),
            (0, 'F'),
        ]
        for cutoff, grade in grades:
            if pct >= cutoff:
                return grade

    def clean_marking(self):
        errors = {}
        if self.mcq > self.subject.mcq_marks:
            errors['mcq'] = "MCQ marks cannot exceed total MCQ marks"
        if self.writing > self.subject.written_marks:
            errors['writing'] = (
                "Writing marks cannot exceed total writing marks"
            )
        if self.practical > self.subject.practical_marks:
            errors['practical'] = (
                "Practical marks cannot exceed total practical marks"
            )

        if errors:
            raise ValidationError(errors)

    def clean_subjects(self):
        if self.subject not in self.aclass.Subject.all():
            raise ValidationError({
                "subject": f"{self.subject.name}\
                is not assigned to class {self.aclass.name}."
            })

    def clean(self):
        self.clean_marking()
        self.clean_subjects()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('student', 'subject', 'exam_type')

    def __str__(self):
        return f"{self.student} –\
            {self.subject.code}: {self.total_marks}/{self.total_possible}"
