from accounts.models import StudentAccount
from django.db import models
from nphs_school.models import Subject


class ResultManager(models.Manager):
    def total_marks_for_student(self, student_id, exam_type):
        results = self.filter(student_id=student_id, type=exam_type)
        return sum(r.total_marks for r in results)

    def total_possible_for_student(self, student_id, exam_type):
        results = self.filter(student_id=student_id, type=exam_type)
        return sum(r.total_possible for r in results)

    def percentage(self, student_id) -> float:
        return (
            (
                self.total_marks_for_student(student_id)
                / float(self.total_possible)
            )
            * 100
            if self.total_possible
            else 0
        )

    # def overall_result(self,student_id,exam_type):
    #     total_obtain_marks=self.total_marks_for_student(student_id,exam_type)
    #     total_possible_marks=self.

    def detail_result(self, result):
        return {
            "mcq": result.mcq,
            "written": result.written,
            "practicle": result.practical,
            "obtained": result.total_marks,
            "percentage": result.percentage,
            "grade": result.grade,
        }

    def student_details(self, student_id):
        student = StudentAccount.objects.get(id=student_id)
        return {
            "student_name": student.account.full_name,
            "student_roll": student.roll_number,
            "religion": student.account.religion,
            "bathc": str(student.batch),
        }

    def subject_details(self, subject_id):
        subject = Subject.objects.get(id=subject_id)
        return {
            "name": subject.name,
            "mcq_total": subject.mcq_marks,
            "written_total": subject.written_marks,
            "practicle_total": subject.practical_marks,
            "total": subject.total_marks,
        }

    def report_card_for(self, student_id, exam_type):
        student = self.student_details(student_id)
        results = self.filter(
            student_id=student_id, exam_type=exam_type
        ).select_related("subject")

        if results is None:
            raise f"sorry no data available for {student_id} or {exam_type}"
        total_obtained = sum(r.total_marks for r in results)
        result_details = []
        total_possible = sum(r.total_possible for r in results)

        for result in results:
            subject_detail = self.subject_details(result.subject_id)
            result_detail = self.detail_result(result)
            result_details.append(
                {
                    "subject": subject_detail,
                    "result": result_detail,
                }
            )

        return {
            "student": student,
            "total_obtained": total_obtained,
            "total_possible": total_possible,
            "percentage": (
                (total_obtained / total_possible * 100)
                if total_possible
                else 0
            ),
            "results": result_details,
        }
