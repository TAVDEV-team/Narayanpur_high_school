from django.shortcuts import render
from rest_framework.viewsets import  ModelViewSet

from accounts.serializers import (
    
    TeacherSerializer, 
    OfficeHelpersSerializer, 
    HeadMasterSerializer, 
    StudentSerializer
    )
from accounts.models import  (
    TeacherAccount, 
    StudentAccount,
    OfficeHelpersAccount, 
    HeadMasterAccount
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
