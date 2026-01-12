from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import StudentAccount

from ..models import Result
from ..serializers import ResultSerializer
from .report_card import generate_report_card_pdf


# @method_decorator(cache_page(60 * 5), name="list")
# @method_decorator(cache_page(60 * 5), name="retrieve")
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        exam = self.request.query_params.get('exam')
        subject = self.request.query_params.get('subject')
        student = self.request.query_params.get('student')
        if exam:
            qs = qs.filter(exam=exam)
        if subject:
            qs = qs.filter(subject=subject)
        if student:
            qs = qs.filter(student=student)
        return qs

    @action(
        detail=False,
        methods=["get"],
        url_path=r"card/(?P<exam_id>[^/.]+)/(?P<class_id>[^/.]+)/(?P<student_id>[^/.]+)",  # noqa: E501
    )
    @method_decorator(cache_page(60 * 5))
    def report_card(
        self, request, student_id=None, exam_id=None, class_id=None
    ):
        student = get_object_or_404(StudentAccount, id=student_id)
        report = Result.objects.report_card_for(student.id, exam_id, class_id)
        return Response(report, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"card_pdf/(?P<exam_id>[^/.]+)/(?P<class_id>[^/.]+)/(?P<student_id>[^/.]+)",  # noqa: E501
    )
    @method_decorator(cache_page(60 * 5))
    def report_card_pdf(
        self, request, student_id=None, exam_id=None, class_id=None
    ):
        student = get_object_or_404(StudentAccount, id=student_id)
        report = Result.objects.report_card_for(student.id, exam_id, class_id)

        # Generate the PDF content
        pdf_content = generate_report_card_pdf(report)

        # Return the PDF as an HttpResponse
        pdf_response = HttpResponse(
            pdf_content, content_type='application/pdf'
        )
        pdf_response['Content-Disposition'] = (
            f'attachment; filename="{report['student']['class']}_{report['student']['roll']}_{report['exam']}.pdf"'  # noqa: E501
        )

        return pdf_response

    @action(
        detail=False,
        methods=['get'],
        url_path=r"class_result/(?P<exam_id>[^/.]+)/(?P<class_id>[^/.]+)",
    )
    # @method_decorator(cache_page(60 * 5))
    def class_result_summary(self, request, class_id=None, exam_id=None):
        result = Result.objects.class_result(class_id, exam_id)
        return Response(result)
