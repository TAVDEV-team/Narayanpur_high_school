from accounts.models import StudentAccount
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Result
from .serializers import ResultSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    @action(detail=False, methods=["get"], url_path="card/(?P<id>[^/.]+)")
    def report_card(self, request, id=None):
        student = get_object_or_404(StudentAccount, id=id)
        report = Result.objects.report_card_for(student.id)
        return Response(report, status=status.HTTP_200_OK)
