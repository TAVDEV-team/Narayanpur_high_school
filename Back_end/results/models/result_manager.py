from django.db import models
from django.db.models import F, Max, Sum

from accounts.models import StudentAccount
from nphs_school.models import About, Subject

from .exam import Exam


class ResultManager(models.Manager):
    # ---------- AGGREGATE QUERIES ----------
    def total_marks_for_student(self, student_id, exam_id):
        # Now filter by exam_id (ForeignKey to Exam)
        results = self.filter(student_id=student_id, exam_id=exam_id)
        return sum(r.total_marks for r in results)

    def total_possible_for_student(self, student_id, exam_id):
        # Now filter by exam_id (ForeignKey to Exam)
        results = self.filter(student_id=student_id, exam_id=exam_id)
        return sum(r.total_possible for r in results)

    def percentage(self, student_id, exam_id) -> float:
        total_possible = self.total_possible_for_student(student_id, exam_id)
        return (
            (
                self.total_marks_for_student(student_id, exam_id)
                / float(total_possible)
            )
            * 100
            if total_possible
            else 0
        )

    def highest_score_of_subject(self, aclass, subject):
        # Annotating total_marks and then applying aggregation
        return (
            self.filter(aclass=aclass, subject=subject)
            .annotate(total_marks=F('mcq') + F('practical') + F('written'))
            .aggregate(Max('total_marks'))['total_marks__max']
        )

    def class_rank(self, student, exam_id):
        """
        Get the class rank for a student based on total marks in the exam.
        """
        # Step 2: Get the class of the student
        student_class = student.batch.current_class

        # Step 3: Aggregate total marks for all students in the class
        results_qs = (
            self.filter(
                exam_id=exam_id, student__batch__current_class=student_class
            )
            .values('student')
            .annotate(
                total_marks=Sum(F('mcq') + F('practical') + F('written'))
            )
            .order_by('-total_marks')
        )

        # Step 4: Find the student's total marks
        student_result = results_qs.get(student=student)
        student_total_marks = student_result['total_marks']

        # Step 5: Rank the student within the class
        rank = 1
        for result in results_qs:
            if result['total_marks'] > student_total_marks:
                rank += 1
            else:
                break

        return rank

    # def highest_score(self, student, exam_id):
    #     """
    #     Get the highest scoring student in the class for a given exam.
    #     """
    #     aclass=student.batch.current_class
    #     highest_result = self.filter(exam_id=exam_id, aclass=aclass) \
    #                          .annotate(total_marks=F('mcq') + F('practical') + F('written')) \  # noqa: E501
    #                          .order_by('-total_marks') \
    #                          .first()

    #     return highest_result
    # ---------- DETAIL BUILDERS ----------
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
        return {
            "name": student.account.full_name,
            "class": student.batch.current_class.name,
            "roll": student.roll_number,
            "religion": student.account.religion,
            "batch": str(student.batch),
            'date_of_birth': student.account.date_of_birth,
            'gender': student.account.gender,
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
            raise f"sorry the {student} is not assigned to any class"

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
    def report_card_for(self, student_id, exam_id):
        student = StudentAccount.objects.get(id=student_id)
        subject_list = self.subjects_of_class(student)
        student_details = self.student_details(student)

        results_qs = self.filter(
            student_id=student_id, exam_id=exam_id
        ).select_related("subject")
        results_map = {res.subject_id: res for res in results_qs}

        result_details = []
        total_obtained = 0
        total_possible = 0
        status = "PASSED"
        for subject in subject_list:
            result = results_map.get(subject.id)
            highest = self.highest_score_of_subject(
                student.batch.current_class, subject
            )
            if result:
                obtained = result.total_marks
                possible = result.total_possible
                detail = self.detail_result(result)
                if detail["grade"] == 'F':
                    status = "FAILED"
            else:
                status = "FAILED"
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
                    "highest_score": highest if highest else 0,
                }
            )
        school = About.objects.get(id=1)
        school_name = school.name
        school_eiin = school.eiin
        school_address = school.location_address
        return {
            "school": school_name,
            "eiin": school_eiin,
            "address": school_address,
            "exam": Exam.objects.get(id=exam_id).exam_title.title(),
            "student": student_details,
            "total_obtained": total_obtained,
            "total_possible": total_possible,
            "status": status,
            "class_rank": self.class_rank(student, exam_id),
            # "highest_score":self.highest_score(student,exam_id),
            "percentage": (
                round((total_obtained / total_possible * 100), 2)
                if total_possible
                else 0
            ),
            "results": result_details,
        }
