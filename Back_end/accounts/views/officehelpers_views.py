from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet

from accounts.models import OfficeHelpersAccount
from accounts.permissions import IsHeadmasterSafe
from accounts.serializers import OfficeHelpersSerializer


@method_decorator(cache_page(60 * 5), name="list")
@method_decorator(cache_page(60 * 5), name="retrieve")
class OfficeHelpersAccountViewSet(ModelViewSet):
    queryset = OfficeHelpersAccount.objects.all().order_by('account')
    serializer_class = OfficeHelpersSerializer
    permission_classes = [IsHeadmasterSafe]
