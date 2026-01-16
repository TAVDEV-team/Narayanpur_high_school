from rest_framework import serializers
from results.models import StudentResult

class FastClassResultSerializer(serializers.ModelSerializer):
    roll = serializers.IntegerField(source="student.roll_number")
    name = serializers.CharField(source="student.account.full_name")

    obtained = serializers.IntegerField(source="total_obtained")
    total = serializers.IntegerField(source="total_possible")

    class Meta:
        model = StudentResult
        fields = [
            "roll",
            "name",
            "obtained",
            "total",
            "percentage",
            "rank",
            "status",
        ]
