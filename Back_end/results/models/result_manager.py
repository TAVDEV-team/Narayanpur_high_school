from django.db import models

from accounts.models import StudentAccount
from nphs_school.models import Subject


class ResultManager(models.Manager):
    # ---------- AGGREGATE QUERIES ----------
    def total_marks_for_student(self, student_id, exam_type):
        results = self.filter(student_id=student_id, exam_type=exam_type)
        return sum(r.total_marks for r in results)

    def total_possible_for_student(self, student_id, exam_type):
        results = self.filter(student_id=student_id, exam_type=exam_type)
        return sum(r.total_possible for r in results)

    def percentage(self, student_id, exam_type) -> float:
        total_possible = self.total_possible_for_student(student_id, exam_type)
        return (
            (
                self.total_marks_for_student(student_id, exam_type)
                / float(total_possible)
            )
            * 100
            if total_possible
            else 0
        )

    # ---------- DETAIL BUILDERS ----------
    def detail_result(self, result):
        print(result)
        return {
            "mcq": result.mcq,
            "written": result.written,
            "practical": result.practical,
            "obtained": result.total_marks,
            "percentage": result.percentage,
            "grade": result.grade,
        }

    def student_details(self, student):
        return {
            "student_name": student.account.full_name,
            "student_roll": student.roll_number,
            "religion": student.account.religion,
            "batch": str(student.batch),
        }

    def subject_details(self, subject_id):
        subject = Subject.objects.get(id=subject_id)
        return {
            "name": subject.name,
            "mcq_total": subject.mcq_marks,
            "written_total": subject.written_marks,
            "practical_total": subject.practical_marks,
            "total": subject.total_marks,
        }

    # ---------- SUBJECT LIST BUILDER ----------
    def subjects_of_class(self, student):
        student_class = student.batch.current_class
        if student_class is None:
            raise f"sorry the {student} is not assaigned to any class"

        # Start with direct class subjects
        subject_list = list(student_class.compulsory.all()) + list(
            student_class.group_subjects.all()
        )

        # Religion-specific subject
        code_map = {
            "islam": "111",
            "hindu": "112",
            "buddhist": "113",
            "christian": "114",
        }
        reli = student.account.religion
        if reli in code_map:
            sub = Subject.objects.filter(code=code_map[reli]).first()
            if sub:
                subject_list.append(sub)

        # Extra subjects
        subject_list.extend(student_class.extra.all())

        return subject_list

    # ---------- REPORT CARD ----------
    def report_card_for(self, student_id, exam_type):
        student = StudentAccount.objects.get(id=student_id)
        subject_list = self.subjects_of_class(student)
        student_details = self.student_details(student)

        # Get all results for this student + exam type
        results_qs = self.filter(
            student_id=student_id, exam_type=exam_type
        ).select_related("subject")
        results_map = {
            res.subject_id: res for res in results_qs
        }  # dict for fast lookup

        result_details = []
        total_obtained = 0
        total_possible = 0

        for subject in subject_list:
            # Try to get existing result, otherwise make a "zero" placeholder
            result = results_map.get(subject.id)
            if result:
                obtained = result.total_marks
                possible = result.total_possible
                detail = self.detail_result(result)
            else:
                obtained = 0
                possible = subject.total_marks
                detail = {
                    "mcq": 0,
                    "written": 0,
                    "practical": 0,
                    "obtained": 0,
                    "percentage": 0,
                    "grade": None,
                }

            total_obtained += obtained
            total_possible += possible

            result_details.append(
                {
                    "subject": self.subject_details(subject.id),
                    "result": detail,
                }
            )

        return {
            "student": student_details,
            "total_obtained": total_obtained,
            "total_possible": total_possible,
            "percentage": (
                round((total_obtained / total_possible * 100), 2)
                if total_possible
                else 0
            ),
            "results": result_details,
        }
