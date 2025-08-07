from django.db import models


class ResultManager(models.Manager):
    def total_marks_for_student(self, student_id):
        results = self.filter(student_id=student_id)
        return sum(r.total_marks for r in results)

    def total_possible_for_student(self, student_id):
        results = self.filter(student_id=student_id)
        return sum(r.total_possible for r in results)

    def report_card_for(self, student_id):
        results = self.filter(student_id=student_id).select_related("subject")
        total_obtained = sum(r.total_marks for r in results)
        total_possible = sum(r.total_possible for r in results)
        return {
            "total_obtained": total_obtained,
            "total_possible": total_possible,
            "percentage": (
                (total_obtained / total_possible * 100)
                if total_possible
                else 0
            ),
        }

    def detailed_report_card_for(self, student_id):
        results = self.filter(student_id=student_id).select_related("subject")
        return [
            {
                "subject": result.subject.name,
                "obtained": result.total_marks,
                "possible": result.total_possible,
                "percentage": result.percentage,
                "grade": result.grade,
            }
            for result in results
        ]
