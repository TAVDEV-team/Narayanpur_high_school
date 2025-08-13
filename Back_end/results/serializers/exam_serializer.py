from rest_framework import serializers

from results.models import Exam


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"
