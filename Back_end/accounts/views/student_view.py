from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from accounts.models import StudentAccount
from accounts.serializers import StudentSerializer, StudentListSerializer


@method_decorator(cache_page(60 * 5), name="list")  # cache list view 5 mins
@method_decorator(
    cache_page(60 * 5), name="retrieve"
)  # cache detail view 5 mins
class StudentAccountViewSet(ModelViewSet):
    queryset = StudentAccount.objects.all().order_by('roll_number')
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return StudentListSerializer
        return StudentSerializer
