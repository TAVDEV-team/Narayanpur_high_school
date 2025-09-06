from rest_framework import serializers

from nphs_school.models import About


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"
