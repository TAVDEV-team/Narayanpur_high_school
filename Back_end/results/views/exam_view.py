from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from ..models import Exam
from ..serializers import ExamSerializer


@method_decorator(cache_page(60 * 5), name="list")
@method_decorator(cache_page(60 * 5), name="retrieve")
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all().order_by('created_at')
    serializer_class = ExamSerializer
    permission_classes = [AllowAny]
