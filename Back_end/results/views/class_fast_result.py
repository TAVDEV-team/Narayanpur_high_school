from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count
from results.models import StudentResult
from results.serializers.result_fast import FastClassResultSerializer
from results.models import Exam  
from nphs_school.models import AClass


class ClassFastResultAPIView(APIView):
    """
    Returns all student results for a class + exam in frontend-compatible format
    """

    def get(self, request, class_id, exam_id):
        # Fetch class and exam titles
        cls = AClass.objects.get(id=class_id)
        exam = Exam.objects.get(id=exam_id)

        # Query all student results for this class+exam
        queryset = StudentResult.objects.filter(
            aclass_id=class_id, exam_id=exam_id
        ).select_related("student").order_by("rank")

        serializer = FastClassResultSerializer(queryset, many=True)

        # Class stats
        total_students = queryset.count()
        passed = queryset.filter(status="PASSED").count()
        failed = queryset.filter(status="FAILED").count()
        overall_percentage = queryset.aggregate(avg=Avg("percentage"))["avg"] or 0.0

        # Total marks of the exam
        total_marks = queryset.first().total_possible if queryset.exists() else 0

        return Response({
    "class": str(cls.name),
    "exam": exam.exam_title,
    "total_students": total_students,
    "total_marks": total_marks,
    "overall_percentage": round(overall_percentage, 2),
    "passed": passed,
    "failed": failed,
    "student_results": [
        {
            "id": s.id,
            "name": getattr(s.student.account, "full_name", "N/A"),  # ✅ correct path
            "roll": getattr(s.student, "roll_number", "N/A"),        # ✅ correct path
            "rank": s.rank,
            "obtained": s.total_obtained,
            "total_marks": s.total_possible,
            "percentage": round(s.percentage, 2),
            "status": s.status,
        } for s in queryset
    ]
})

