from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet

from accounts.models import HeadMasterAccount
from accounts.permissions import IsHeadmasterSafe
from accounts.serializers import HeadMasterSerializer


@method_decorator(cache_page(60 * 5), name="list")
@method_decorator(cache_page(60 * 5), name="retrieve")
class HeadMasterAccountViewSet(ModelViewSet):
    queryset = HeadMasterAccount.objects.all()
    serializer_class = HeadMasterSerializer
    permission_classes = [IsHeadmasterSafe]
