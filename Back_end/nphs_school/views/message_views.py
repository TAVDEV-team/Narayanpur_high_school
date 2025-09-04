from rest_framework import viewsets

from nphs_school.models import Messages
from accounts.permissions import IsTeacher
from nphs_school.serializers import MessagesSerializer


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = [IsTeacher]
