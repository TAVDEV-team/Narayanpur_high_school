from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from nphs_school.models import Messages
from nphs_school.permissions import MessagesPermission
from nphs_school.serializers import MessagesSerializer


@method_decorator(cache_page(60 * 60 * 24 * 10), name="list")
@method_decorator(cache_page(60 * 60 * 24 * 10), name="retrieve")
class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all().order_by('created_at')
    serializer_class = MessagesSerializer
    permission_classes = [MessagesPermission]
