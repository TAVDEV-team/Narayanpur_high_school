from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet

from accounts.models import TeacherAccount
from accounts.permissions import IsHeadmasterSafe
from accounts.serializers import TeacherSerializer


@method_decorator(cache_page(60 * 5), name="list")
@method_decorator(cache_page(60 * 5), name="retrieve")
class TeacherAccountViewSet(ModelViewSet):
    queryset = TeacherAccount.objects.all().order_by('account')
    serializer_class = TeacherSerializer
    permission_classes = [IsHeadmasterSafe]
