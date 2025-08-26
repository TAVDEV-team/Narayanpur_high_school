from django.db import models
from django.db.models import F, Max, Sum
from django.shortcuts import get_object_or_404

from accounts.models import StudentAccount
from nphs_school.models import About, AClass, Subject

from .exam import Exam


class ResultManager(models.Manager):
    # ---------------- AGGREGATE QUERIES ----------------

    def total_marks_for_student(self, student_id, exam_id):
        return (
            self.filter(student_id=student_id, exam_id=exam_id).aggregate(
                total=Sum(F('mcq') + F('written') + F('practical'))
            )['total']
            or 0
        )

    def total_possible_for_student(self, student_id, exam_id):
        return (
            self.filter(student_id=student_id, exam_id=exam_id).aggregate(
                total=Sum(
                    F('subject__mcq_marks')
                    + F('subject__written_marks')
                    + F('subject__practical_marks')
                )
            )['total']
            or 0
        )

    def percentage(self, student_id, exam_id) -> float:
        total_possible = self.total_possible_for_student(student_id, exam_id)
        if total_possible == 0:
            return 0
        total_obtained = self.total_marks_for_student(student_id, exam_id)
        return round((total_obtained / total_possible) * 100, 2)

    def highest_score_of_subject(self, aclass, subject):
        return (
            self.filter(aclass=aclass, subject=subject)
            .annotate(total_marks=F('mcq') + F('practical') + F('written'))
            .aggregate(Max('total_marks'))['total_marks__max']
            or 0
        )

    def class_rank(self, student, exam_id, class_id):
        student_class = AClass.objects.get(id=class_id)
        results_qs = (
            self.filter(exam_id=exam_id, student__batch=student_class.batch)
            .values('student')
            .annotate(
                total_marks=Sum(F('mcq') + F('written') + F('practical'))
            )
            .order_by('-total_marks')
        )
        student_total = next(
            (
                r['total_marks']
                for r in results_qs
                if r['student'] == student.id
            ),
            0,
        )

        rank = 1
        for res in results_qs:
            if res['total_marks'] > student_total:
                rank += 1
            else:
                break
        return rank

    # ---------------- DETAIL BUILDERS ----------------

    def detail_result(self, result):
        return {
            "mcq": result.mcq,
            "written": result.written,
            "practical": result.practical,
            "obtained": result.total_marks,
            "percentage": result.percentage,
            "grade": result.grade,
        }

    def student_details(self, student):
        current_class = getattr(student.batch, 'current_class', None)
        return {
            'id': student.id,
            "name": student.account.full_name.title(),
            "class": current_class.name if current_class else None,
            "roll": student.roll_number,
            "religion": student.account.religion.title(),
            "batch": str(student.batch),
            'date_of_birth': student.account.date_of_birth,
            'gender': student.account.gender.title(),
        }

    def subject_details(self, subject):
        return {
            "name": subject.name,
            "mcq_total": subject.mcq_marks,
            "written_total": subject.written_marks,
            "practical_total": subject.practical_marks,
            "total": subject.total_marks,
        }

    # ---------------- SUBJECT LIST ----------------

    def subjects_of_class(self, student, class_id):
        student_class = AClass.objects.get(id=class_id)
        if not student_class:
            raise ValueError(f"{student} is not assigned to any class")

        subjects = list(student_class.compulsory.all()) + list(
            student_class.group_subjects.all()
        )
        code_map = {
            "islam": "111",
            "hindu": "112",
            "buddhist": "113",
            "christian": "114",
        }
        religion_code = code_map.get(student.account.religion)
        if religion_code:
            sub = Subject.objects.filter(code=religion_code).first()
            if sub:
                subjects.append(sub)

        subjects.extend(student_class.extra.all())
        return subjects

    # ---------------- REPORT CARD ----------------

    def report_card_for(self, student_id, exam_id, class_id):
        student = StudentAccount.objects.get(id=student_id)
        subjects = self.subjects_of_class(student, class_id)
        student_info = self.student_details(student)

        results_qs = self.filter(
            student_id=student_id, exam_id=exam_id
        ).select_related("subject")
        results_map = {res.subject_id: res for res in results_qs}

        total_obtained = total_possible = 0
        status = "PASSED"
        result_details = []

        for sub in subjects:
            result = results_map.get(sub.id)
            if result:
                obtained = result.total_marks
                possible = result.total_possible
                detail = self.detail_result(result)
                if detail["grade"] == 'F':
                    status = "FAILED"
            else:
                obtained = 0
                possible = sub.total_marks
                detail = {
                    "mcq": 0,
                    "written": 0,
                    "practical": 0,
                    "obtained": 0,
                    "percentage": 0,
                    "grade": 'F',
                }
                status = "FAILED"

            total_obtained += obtained
            total_possible += possible

            result_details.append(
                {
                    "subject": self.subject_details(sub),
                    "result": detail,
                    "highest_score": self.highest_score_of_subject(
                        student.batch.current_class, sub
                    ),
                }
            )

        school = About.objects.get(id=1)
        exam_title = Exam.objects.get(id=exam_id).exam_title.title()
        return {
            "school": school.name,
            "eiin": school.eiin,
            "address": school.location_address,
            "exam": exam_title,
            "student": student_info,
            "total_obtained": total_obtained,
            "total_possible": total_possible,
            "status": status,
            "class_rank": self.class_rank(student, exam_id, class_id),
            "percentage": (
                round((total_obtained / total_possible * 100), 2)
                if total_possible
                else 0
            ),
            "results": result_details,
        }

    # ---------------- CLASS RESULT SUMMARY ----------------

    def class_result(self, class_id, exam_id):
        aclass = get_object_or_404(AClass, id=class_id)
        students = StudentAccount.objects.filter(batch=aclass.batch)
        exam = Exam.objects.get(id=exam_id)
        total_students = len(students)
        passed = 0
        failed = 0
        overall_percentage = 0
        total_marks = 0
        class_results = []
        for student in students:
            report_data = self.report_card_for(student.id, exam_id, class_id)
            student_id = report_data['student']['id']
            name = report_data['student']['name']
            roll = report_data['student']['roll']
            rank = report_data['class_rank']
            obtained = report_data['total_obtained']
            percentage = report_data['percentage']
            status = report_data['status']
            if total_marks == 0:
                total_marks = report_data['total_possible']
            overall_percentage += percentage

            if status == "FAILED":
                failed += 1
            else:
                passed += 1

            data = {
                'id': student_id,
                'name': name,
                'roll': roll,
                'rank': rank,
                'obtained': obtained,
                'percentage': percentage,
                'status': status,
            }
            class_results.append(data)
        if overall_percentage != 0:
            overall_percentage /= total_students

        return {
            'class': aclass.name,
            'exam': exam.exam_title,
            'total_students': total_students,
            'total_marks': total_marks,
            'overall_percentage': overall_percentage,
            'passed': passed,
            'failed': failed,
            'student_results': class_results,
        }
