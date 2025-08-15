from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import StudentAccount
from accounts.serializers import StudentSerializer
from nphs_school.models import AClass
from nphs_school.serializers import AClassSerializer


class AClassViewSet(viewsets.ModelViewSet):
    queryset = AClass.objects.all()
    serializer_class = AClassSerializer

    @action(detail=True, methods=["get"], url_path="detail")
    def get_detail(self, request, pk=None):
        aclass = self.get_object()
        students = StudentAccount.objects.filter(batch__current_class=aclass)
        student_serializer = StudentSerializer(students, many=True)

        return Response(
            {
                "aclass": self.get_serializer(aclass).data,
                "students": student_serializer.data,
            }
        )
