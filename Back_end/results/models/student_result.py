# from django.db import models


# class StudentResult(models.Model):
#     """
#     student = whos result?
#     class= from which class? (also for using as history)
#     all subjects = which subjects werer there?
#     total_marks for that class
#     """


from django.db import models
from accounts.models import StudentAccount
from nphs_school.models import AClass
from results.models.exam import Exam


class StudentResult(models.Model):
    STATUS_CHOICES = (
        ("PASSED", "Passed"),
        ("FAILED", "Failed"),
    )

    student = models.ForeignKey(
        StudentAccount,
        on_delete=models.CASCADE,
        related_name="student_results",
        db_index=True,
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="student_results",
        db_index=True,
    )
    aclass = models.ForeignKey(
        AClass,
        on_delete=models.CASCADE,
        related_name="student_results",
        db_index=True,
    )

    total_obtained = models.PositiveIntegerField()
    total_possible = models.PositiveIntegerField()

    percentage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        db_index=True,
    )

    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        db_index=True,
    )

    rank = models.PositiveIntegerField(db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["student", "exam", "aclass"],
    #             name="unique_student_exam_class_result",
    #         )
    #     ]
    #     indexes = [
    #         models.Index(fields=["aclass", "exam"]),
    #         models.Index(fields=["aclass", "exam", "rank"]),
    #     ]
    #     ordering = ["rank", "student__roll_number"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "exam"],
                name="unique_student_exam_result",
            )
        ]
        indexes = [
            models.Index(fields=["exam", "aclass"]),
            models.Index(fields=["exam", "rank"]),
            models.Index(fields=["aclass", "rank"]),
        ]
        ordering = ["rank"]


    def __str__(self):
        return (
            f"{self.student.roll_number} | "
            f"{self.aclass.name} | "
            f"{self.exam.exam_title} | "
            f"Rank {self.rank}"
        )
