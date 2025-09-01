from rest_framework import viewsets

from nphs_school.models import Messages
from nphs_school.serializers import MessagesSerializer


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
