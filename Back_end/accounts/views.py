from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import (
    HeadMasterAccount,
    OfficeHelpersAccount,
    StudentAccount,
    TeacherAccount,
)
from accounts.serializers import (
    HeadMasterSerializer,
    OfficeHelpersSerializer,
    StudentSerializer,
    TeacherSerializer,
)


class TeacherAccountViewSet(ModelViewSet):
    queryset = TeacherAccount.objects.all()
    serializer_class = TeacherSerializer


class StudentAccountViewSet(ModelViewSet):
    queryset = StudentAccount.objects.all()
    serializer_class = StudentSerializer


class OfficeHelpersAccountViewSet(ModelViewSet):
    queryset = OfficeHelpersAccount.objects.all()
    serializer_class = OfficeHelpersSerializer


class HeadMasterAccountViewSet(ModelViewSet):
    queryset = HeadMasterAccount.objects.all()
    serializer_class = HeadMasterSerializer


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Access the token from the Authorization header
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklisting the token
            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": f"Invalid token {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
