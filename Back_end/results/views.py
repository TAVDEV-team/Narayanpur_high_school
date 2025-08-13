from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import StudentAccount

from .models import Exam, Result
from .serializers import ExamSerializer, ResultSerializer


def generate_report_card_pdf(report_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Prepare content (title, student info, table data)
    content = []

    # Title Styling
    title_style = styles['Title']
    title_style.fontSize = 28
    title_style.alignment = 1  # Center-aligned
    title_style.spaceAfter = 10  # Space after title

    title = Paragraph("NARAYANPUR HIGH SCHOOL", title_style)
    content.append(title)

    # Subtitle Styling
    sub_title_style = styles['Title']
    sub_title_style.fontSize = 12
    sub_title_style.alignment = 1  # Center-aligned
    sub_title_style.spaceAfter = 10
    content.append(
        Paragraph("Amjad Nagar, Chaddagram, Cumilla 3500", sub_title_style)
    )
    exam = Paragraph(f"{report_data['exam'].title()}", sub_title_style)
    content.append(exam)

    # Student Information Styling
    about_style = styles['Normal']
    about_style.fontSize = 10
    about_style.alignment = 0  # Left-aligned
    about_style.spaceAfter = 2  # Space after each line
    about_style.fontName = 'Helvetica-Bold'

    for key in ['name', 'class', 'roll', 'date_of_birth', 'religion']:
        content.append(
            Paragraph(
                f"{key.replace('_', ' ').title()}: {report_data['student'][key]}",  # noqa: E501
                about_style,
            )
        )
    content.append(Paragraph('', title_style))
    content.append(Paragraph('', title_style))
    # Adding table for results
    table_data = [
        [
            "Subject",
            "MCQ",
            "Written",
            "Practical",
            "Obtained",
            "Highest",
            "Grade",
            "Percentage",
        ]
    ]

    for res in report_data['results']:
        hs = res['highest_score']

        subj = res['subject']['name'].title()
        if subj == "English 2Nd Paper (6-8)":
            subj = "English 2Nd Paper"

        if subj == "Bangla 2Nd (6-8)":
            subj = "Bangla 2nd"

        mcq = res['result']['mcq']
        written = res['result']['written']
        practical = res['result']['practical']
        obtained = res['result']['obtained']
        grade = res['result']['grade'] or "F"
        percentage = f"{res['result']['percentage']}%"
        table_data.append(
            [subj, mcq, written, practical, obtained, hs, grade, percentage]
        )

    # Creating table with styled cells
    table = Table(table_data, colWidths=[130, 60, 60, 60, 60, 60, 60, 60])

    table.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                (
                    'ALIGN',
                    (1, 0),
                    (-1, -1),
                    'CENTER',
                ),  # Center-align all the data
                ('ALIGN', (1, 0), (0, -1), 'LEFT'),
            ]
        )
    )

    # Adding the table to the content
    content.append(table)
    content.append(Paragraph('', title_style))
    content.append(Paragraph('', title_style))
    table_data = [["Total", "Obtained", "Rank", "Percentage", "Status"]]
    table_data.append(
        [
            report_data['total_possible'],
            report_data['total_obtained'],
            report_data['class_rank'],
            f"{report_data['percentage']}%",
            report_data['status'],
        ]
    )
    table = Table(table_data, colWidths=[110, 110, 110, 110, 110])
    table.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                (
                    'ALIGN',
                    (1, 0),
                    (-1, -1),
                    'CENTER',
                ),  # Center-align all the data
                ('ALIGN', (1, 0), (0, -1), 'LEFT'),
            ]
        )
    )
    content.append(table)

    content.append(Paragraph('', title_style))
    content.append(Paragraph('', title_style))
    content.append(Paragraph('', title_style))
    content.append(Paragraph('-------------------------', about_style))
    content.append(Paragraph('Gurdian Signature', about_style))
    # Finalizing the PDF
    doc.build(content)

    # Get the PDF content from the buffer
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
            pdf_content, content_type='application/pdf'
        )
        pdf_response['Content-Disposition'] = (
            f'attachment; filename="{report['student']['class']}_{report['student']['roll']}_{report['exam']}.pdf"'  # noqa: E501
        )

        return pdf_response


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
