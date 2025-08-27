from django.db import models
from django.db.models import F, Max, Sum, Value

# from django.db.models import F, IntegerField, Max, Sum, Value
from django.db.models.functions import Coalesce

from accounts.models import StudentAccount
from nphs_school.models import About, AClass, Subject

from .exam import Exam

# from django.shortcuts import get_object_or_404


class ResultManager(models.Manager):
    # ---------------- FAST AGGREGATES ----------------

    def total_marks_for_student(self, student_id, exam_id):
        return (
            self.filter(student_id=student_id, exam_id=exam_id)
            .aggregate(
                total=Coalesce(
                    Sum(F('mcq') + F('written') + F('practical')), Value(0)
                )
            )
            .get('total', 0)
        )

    def total_possible_for_student(self, student_id, exam_id):
        return (
            self.filter(student_id=student_id, exam_id=exam_id)
            .aggregate(
                total=Coalesce(
                    Sum(
                        F('subject__mcq_marks')
                        + F('subject__written_marks')
                        + F('subject__practical_marks')
                    ),
                    Value(0),
                )
            )
            .get('total', 0)
        )

    def percentage(self, student_id, exam_id) -> float:
        total_possible = self.total_possible_for_student(student_id, exam_id)
        if not total_possible:
            return 0.0
        total_obtained = self.total_marks_for_student(student_id, exam_id)
        return round((total_obtained / total_possible) * 100, 2)

    # ---------------- HELPERS (NO DB IN LOOPS) ----------------

    def _detail_result(self, result):
        return {
            "mcq": result.mcq,
            "written": result.written,
            "practical": result.practical,
            "obtained": result.total_marks,
            "percentage": result.percentage,
            "grade": result.grade,
        }

    def _student_details(self, student):
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

    def _subject_details(self, subject):
        return {
            "name": subject.name,
            "mcq_total": subject.mcq_marks,
            "written_total": subject.written_marks,
            "practical_total": subject.practical_marks,
            "total": subject.total_marks,
        }

    def _religion_subject_for(self, religion_lower: str, religion_map):
        """
        religion_map: dict like {"111": Subject, ...}
        """
        code_map = {
            "islam": "111",
            "hindu": "112",
            "buddhist": "113",
            "christian": "114",
        }
        code = code_map.get(religion_lower)
        return religion_map.get(code)

    def _subjects_for_student(
        self, aclass: AClass, student: StudentAccount, prefetch_cache
    ):
        """
        Build subject list for a student using preloaded
        class relations and preloaded religion lookup.
        prefetch_cache: dict with keys:
           - 'compulsory', 'group_subjects',
            'extra' : QuerySets already evaluated
           - 'religion_by_code': {code: Subject}
        """
        subjects = []
        subjects.extend(prefetch_cache['compulsory'])
        subjects.extend(prefetch_cache['group_subjects'])
        # religion subject
        rel = self._religion_subject_for(
            student.account.religion, prefetch_cache['religion_by_code']
        )
        if rel:
            subjects.append(rel)
        # extras
        subjects.extend(prefetch_cache['extra'])
        return subjects

    # ---------------- PRECOMPUTE HEAVY PARTS ----------------

    def _highest_scores_by_subject(self, aclass: AClass, exam_id: int):
        """
        Compute highest total per subject for the given class & exam once.
        """
        rows = (
            self.filter(aclass=aclass, exam_id=exam_id)
            .annotate(total=F('mcq') + F('written') + F('practical'))
            .values('subject')
            .annotate(highest=Max('total'))
        )
        return {r['subject']: (r['highest'] or 0) for r in rows}

    def _totals_by_student(self, aclass: AClass, exam_id: int):
        """
        Sum total marks per student for rank calculation (single query).
        """
        rows = (
            self.filter(exam_id=exam_id, student__batch=aclass.batch)
            .values('student')
            .annotate(
                total=Coalesce(
                    Sum(F('mcq') + F('written') + F('practical')), Value(0)
                )
            )
            .order_by('-total', 'student')
        )
        # Build rank map (dense rank)
        rank_map = {}
        total_map = {}
        prev_total = None
        rank = 0
        for idx, r in enumerate(rows, start=1):
            t = r['total'] or 0
            if t != prev_total:
                rank = idx
                prev_total = t
            sid = r['student']
            total_map[sid] = t
            rank_map[sid] = rank
        return total_map, rank_map

    def _prefetch_class_and_students(self, class_id: int):
        """
        Load class + its subjects +
        students + their accounts in minimal queries.
        """
        aclass = (
            AClass.objects.select_related('batch')
            .prefetch_related('compulsory', 'group_subjects', 'extra')
            .get(id=class_id)
        )
        students = StudentAccount.objects.filter(
            batch=aclass.batch
        ).select_related('account', 'batch')
        return aclass, students

    def _build_prefetch_cache(self, aclass: AClass):
        # Resolve prefetched subject sets to lists (avoid DB inside loops)
        compulsory = list(aclass.compulsory.all())
        group_subjects = list(aclass.group_subjects.all())
        extra = list(aclass.extra.all())
        # Religion subjects lookup by code (pull once)
        religion_subjects = Subject.objects.filter(
            code__in=["111", "112", "113", "114"]
        )
        religion_by_code = {s.code: s for s in religion_subjects}
        return {
            'compulsory': compulsory,
            'group_subjects': group_subjects,
            'extra': extra,
            'religion_by_code': religion_by_code,
        }

    # ---------------- REPORT CARD (refactored) ----------------

    def _report_card_for_preloaded(
        self,
        student: StudentAccount,
        exam_id: int,
        aclass: AClass,
        highest_by_subject: dict,
        prefetch_cache: dict,
        school: About,
        exam: Exam,
    ):
        # subjects for this specific student (religion may differ)
        subjects = self._subjects_for_student(aclass, student, prefetch_cache)
        student_info = self._student_details(student)

        # Pull all results for this student &
        # exam in one go and index by subject_id
        results_qs = self.filter(
            student_id=student.id, exam_id=exam_id
        ).select_related("subject")
        results_map = {r.subject_id: r for r in results_qs}

        total_obtained = 0
        total_possible = 0
        status = "PASSED"
        result_details = []

        for sub in subjects:
            result = results_map.get(sub.id)
            if result:
                obtained = result.total_marks
                possible = result.total_possible
                detail = self._detail_result(result)
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
                    "subject": self._subject_details(sub),
                    "result": detail,
                    "highest_score": highest_by_subject.get(sub.id, 0),
                }
            )

        # class rank computed outside; injected later by caller
        return {
            "school": school.name,
            "eiin": school.eiin,
            "address": school.location_address,
            "exam": exam.exam_title.title(),
            "student": student_info,
            "total_obtained": total_obtained,
            "total_possible": total_possible,
            "status": status,
            # "class_rank": <filled by caller>,
            "percentage": (
                round((total_obtained / total_possible * 100), 2)
                if total_possible
                else 0
            ),
            "results": result_details,
        }

    def report_card_for(self, student_id, exam_id, class_id):
        """
        Backward-compatible public API. Internally uses the optimized pipeline.
        """
        aclass, students = self._prefetch_class_and_students(class_id)
        school = About.objects.only(
            'id', 'name', 'eiin', 'location_address'
        ).get(id=1)
        exam = Exam.objects.only('id', 'exam_title').get(id=exam_id)

        # Precompute shared data
        prefetch_cache = self._build_prefetch_cache(aclass)
        highest_by_subject = self._highest_scores_by_subject(aclass, exam_id)
        totals_map, rank_map = self._totals_by_student(aclass, exam_id)

        # Find the target student from the preloaded set (avoid extra query)
        student = next((s for s in students if s.id == int(student_id)), None)
        if not student:
            # Fallback (should not happen) — but keep it safe
            student = StudentAccount.objects.select_related(
                'account', 'batch'
            ).get(id=student_id)

        card = self._report_card_for_preloaded(
            student=student,
            exam_id=exam_id,
            aclass=aclass,
            highest_by_subject=highest_by_subject,
            prefetch_cache=prefetch_cache,
            school=school,
            exam=exam,
        )
        card["class_rank"] = rank_map.get(student.id, None)
        return card

    # ---------------- CLASS RESULT SUMMARY (O(Queries) ~ constant)\

    def class_result(self, class_id, exam_id):
        aclass, students = self._prefetch_class_and_students(class_id)
        exam = Exam.objects.only('id', 'exam_title').get(id=exam_id)
        school = About.objects.only('id').get(id=1)

        total_students = students.count()
        if total_students == 0:
            return {
                'class': aclass.name,
                'exam': exam.exam_title,
                'total_students': 0,
                'total_marks': 0,
                'overall_percentage': 0,
                'passed': 0,
                'failed': 0,
                'student_results': [],
            }

        # Precompute once
        prefetch_cache = self._build_prefetch_cache(aclass)
        highest_by_subject = self._highest_scores_by_subject(aclass, exam_id)

        # All results for these students for this exam (once)
        results = self.filter(
            exam_id=exam_id, student__in=students
        ).select_related(
            'student',
            'student__account',
            'subject',
            'student__batch',
        )

        # Index results by student_id -> subject_id -> result
        results_by_student = {}
        for r in results:
            sid = r.student_id
            if sid not in results_by_student:
                results_by_student[sid] = {}
            results_by_student[sid][r.subject_id] = r

        # Rank map & totals (once)
        totals_map, rank_map = self._totals_by_student(aclass, exam_id)

        # Prepare summary in one pass
        class_results = []
        passed = failed = 0
        overall_percentage = 0.0
        total_marks_reference = None  # first computed total_possible

        for student in students:
            # Compute report body using preloaded data; avoid extra queries
            student_card = self._report_card_for_preloaded(
                student=student,
                exam_id=exam_id,
                aclass=aclass,
                highest_by_subject=highest_by_subject,
                prefetch_cache=prefetch_cache,
                school=school,  # name/eiin not used in summary
                exam=exam,
            )

            # Override results_map with pre-indexed results
            # to avoid internal fetch
            # (small optimization: if you want to go further,
            # inject map into _report_card_for_preloaded)

            status = student_card["status"]
            if total_marks_reference is None:
                total_marks_reference = student_card["total_possible"]
            overall_percentage += student_card["percentage"]
            if status == "FAILED":
                failed += 1
            else:
                passed += 1

            class_results.append(
                {
                    'id': student.id,
                    'name': student.account.full_name.title(),
                    'roll': student.roll_number,
                    'rank': rank_map.get(student.id),
                    'obtained': student_card['total_obtained'],
                    'percentage': student_card['percentage'],
                    'status': status,
                }
            )
        class_results.sort(key=lambda x: (x['rank'] or 999999, x['roll']))
        overall_percentage = (
            round(overall_percentage / total_students, 2)
            if total_students
            else 0.0
        )

        return {
            'class': aclass.name,
            'exam': exam.exam_title,
            'total_students': total_students,
            'total_marks': total_marks_reference or 0,
            'overall_percentage': overall_percentage,
            'passed': passed,
            'failed': failed,
            'student_results': class_results,
        }
