from rest_framework import viewsets

from nphs_school.models import Messages
from nphs_school.permissions import MessagesPermission
from nphs_school.serializers import MessagesSerializer


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all().order_by('created_at')
    serializer_class = MessagesSerializer
    permission_classes = [MessagesPermission]
