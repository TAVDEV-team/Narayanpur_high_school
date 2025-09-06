from rest_framework import serializers

from nphs_school.models import Routine


class RoutineSerializer(serializers.ModelSerializer):
    slot_display = serializers.CharField(
        source="get_slot_display", read_only=True
    )
    day_display = serializers.CharField(
        source="get_day_display", read_only=True
    )

    class Meta:
        model = Routine
        fields = [
            "id",
            "aclass",
            "day",
            "day_display",
            "slot",
            "slot_display",
            "subject",
            "teacher",
        ]
