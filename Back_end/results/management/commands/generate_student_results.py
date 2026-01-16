from django.core.management.base import BaseCommand
from results.models.result_model import Result
from results.models.student_result import StudentResult
from nphs_school.models import AClass
from results.models.exam import Exam
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce

class Command(BaseCommand):
    help = "Compute and cache class-wise student results"

    def handle(self, *args, **kwargs):
        exams = Exam.objects.all()
        for exam in exams:
            classes = AClass.objects.all()
            for aclass in classes:
                results_qs = Result.objects.filter(
                    exam=exam, aclass=aclass
                ).select_related('student', 'subject')
                
                # compute per student
                student_totals = {}
                for r in results_qs:
                    sid = r.student_id
                    total = r.mcq + r.written + r.practical
                    possible = r.subject.total_marks
                    student_totals.setdefault(sid, {'obtained': 0, 'possible': 0})
                    student_totals[sid]['obtained'] += total
                    student_totals[sid]['possible'] += possible
                
                # sort students by total obtained for rank
                ranked = sorted(student_totals.items(), key=lambda x: -x[1]['obtained'])
                bulk_objs = []
                for idx, (sid, data) in enumerate(ranked, start=1):
                    perc = round((data['obtained'] / data['possible']) * 100, 2)
                    status = 'PASSED' if perc >= 33 else 'FAILED'
                    bulk_objs.append(StudentResult(
                        student_id=sid,
                        exam=exam,
                        aclass=aclass,
                        total_obtained=data['obtained'],
                        total_possible=data['possible'],
                        percentage=perc,
                        status=status,
                        rank=idx,
                    ))
                StudentResult.objects.bulk_create(bulk_objs, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("StudentResult computed successfully"))
