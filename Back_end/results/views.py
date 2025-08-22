from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import StudentAccount

from .models import Exam, Result
from .serializers import ExamSerializer, ResultSerializer


def generate_report_card_pdf(report_data):
    # school =
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Prepare content (title, student info, table data)
    content = []

    # Title Styling
    title_style = styles['Title']
    title_style.fontSize = 28
    title_style.alignment = 1  # Center-aligned
    title_style.spaceAfter = 50  # Space after title

    title = Paragraph(report_data['school'].upper(), title_style)
    content.append(title)

    # Subtitle Styling
    sub_title_style = styles['Title']
    sub_title_style.fontSize = 14
    sub_title_style.alignment = 1  # Center-aligned
    sub_title_style.spaceAfter = 10
    content.append(Paragraph(report_data['address'], sub_title_style))
    exam = Paragraph(f"{report_data['exam'].title()}", sub_title_style)
    content.append(exam)

    # ====== About Section ======
    about_data = [
        ['Name :', report_data['student']['name']],
        ['Class :', report_data['student']['class']],
        ['Roll :', report_data['student']['roll']],
        ['Date Of Birth :', report_data['student']['date_of_birth']],
        ['Religion :', report_data['student']['religion']],
        ['Gender :', report_data['student']['gender']],
    ]

    about_table = Table(about_data, colWidths=[75, 120])
    about_table.setStyle(
        TableStyle(
            [
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),  # Labels bold
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]
        )
    )

    # ====== Summary Section ======
    summary_data = [
        ['Result', 'Summary'],
        ['Total', report_data['total_possible']],
        ['Obtained', report_data['total_obtained']],
        ['Rank', report_data['class_rank']],
        ['Percentage', f"{report_data['percentage']}%"],
        ['Status', report_data['status']],
    ]

    summary_table = Table(summary_data, colWidths=[80, 70])
    summary_table.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    # ====== Hero Grade Table ======
    grades_data = [
        ['Marks', 'Grade'],
        ['80-100', 'A+'],
        ['70-79', 'A'],
        ['60-69', 'A-'],
        ['50-59', 'B'],
        ['40-49', 'C'],
        ['33-39', 'D'],
        ['0-32', 'F'],
    ]

    hero_table = Table(grades_data, colWidths=[65, 65])
    hero_table.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]
        )
    )

    # ====== Combine into one row ======
    final_row = [about_table, summary_table, hero_table]

    final_table = Table([final_row], colWidths=[200, 150, 200])
    final_table.setStyle(
        TableStyle(
            [
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ]
        )
    )

    content.append(final_table)
    content.append(Spacer(1, 10))

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

    content.append(Spacer(1, 20))  # extra space above lines

    data = [
        [
            "....................",
            "............................",
            ".....................",
        ],  # dotted signature lines
        ["Guardian", "Class Teacher", "Head Master"],
    ]

    table = Table(data, colWidths=[170, 175, 170])

    table.setStyle(
        TableStyle(
            [
                # Align labels
                ("ALIGN", (0, 0), (0, 1), "LEFT"),
                ("ALIGN", (1, 0), (1, 1), "CENTER"),
                ("ALIGN", (2, 0), (2, 1), "RIGHT"),
                # Add some padding so lines don't touch text
                ("TOPPADDING", (0, 0), (-1, 0), 15),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ]
        )
    )

    content.append(table)
    # Finalizing the PDF
    doc.build(content)

    # Get the PDF content from the buffer
    pdf = buffer.getvalue()
    buffer.close()

    return pdf


# @method_decorator(cache_page(60 * 5), name="list")
# @method_decorator(cache_page(60 * 5), name="retrieve")
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path=r"card/(?P<exam_id>[^/.]+)/(?P<id>[^/.]+)",
    )
    # @method_decorator(cache_page(60 * 5))
    def report_card(self, request, id=None, exam_id=None):
        student = get_object_or_404(StudentAccount, id=id)
        report = Result.objects.report_card_for(student.id, exam_id)
        return Response(report, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"card_pdf/(?P<exam_id>[^/.]+)/(?P<id>[^/.]+)",
    )
    # @method_decorator(cache_page(60 * 5))
    def report_card_pdf(self, request, id=None, exam_id=None):
        student = get_object_or_404(StudentAccount, id=id)
        report = Result.objects.report_card_for(student.id, exam_id)

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


@method_decorator(cache_page(60 * 5), name="list")
@method_decorator(cache_page(60 * 5), name="retrieve")
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
