from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import StudentAccount

from .models import Result, Exam
from .serializers import ResultSerializer, ExamSerializer


def generate_report_card_pdf(report_data):
    from io import BytesIO

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import (Paragraph, SimpleDocTemplate, Table,
                                    TableStyle)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Prepare content (title, student info, table data)
    content = []

    title_style = styles['Title']
    title_style.fontSize = 18
    title_style.alignment = 1

    title = Paragraph("NARAYANPUR HIGH SCHOOL", title_style)
    content.append(title)
    exam_style = styles['Title']
    exam_style.fontSize = 10
    exam_style.alignment = 1
    exam = Paragraph(f"{report_data['exam']}", exam_style)
    content.append(exam)

    for key in ['student_name', 'class', 'student_roll', 'batch', 'religion']:
        content.append(
            Paragraph(
                f"{key.replace('_', ' ').title()}: {
                    report_data['student'][key]}", styles['Normal']
                )
                )

    table_data = [
        [
            "Subject",
            "MCQ",
            "Written",
            "practical",
            "Obtained",
            "Grade",
            "Percentage"
            ]
        ]
    for res in report_data['results']:
        subj = res['subject']['name']
        mcq = res['result']['mcq']
        practical = res['result']['practical']
        written = res['result']['written']
        obtained = res['result']['obtained']
        grade = res['result']['grade'] or "-"
        percentage = f"{res['result']['percentage']}%"
        table_data.append(
            [subj, mcq, written, practical, obtained, grade, percentage]
            )

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    content.append(table)

    doc.build(content)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path=r"card/(?P<exam_type>[^/.]+)/(?P<id>[^/.]+)",
    )
    def report_card(self, request, id=None, exam_type=None):
        student = get_object_or_404(StudentAccount, id=id)
        report = Result.objects.report_card_for(student.id, exam_type)
        return Response(report, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"card_pdf/(?P<exam_type>[^/.]+)/(?P<id>[^/.]+)",
    )
    def report_card_pdf(self, request, id=None, exam_type=None):
        student = get_object_or_404(StudentAccount, id=id)
        report = Result.objects.report_card_for(student.id, exam_type)

        # Generate the PDF content
        pdf_content = generate_report_card_pdf(report)

        # Return the PDF as an HttpResponse
        pdf_response = HttpResponse(
            pdf_content,
            content_type='application/pdf'
            )
        pdf_response['Content-Disposition'] = (
            f'attachment; filename="report_card_{student.id}_{exam_type}.pdf"'
            )

        return pdf_response


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
