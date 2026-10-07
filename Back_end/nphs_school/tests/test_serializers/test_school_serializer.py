from nphs_school.models import School
from nphs_school.serializers.school_serializer import SchoolSerializer

from .common_serializer import BaseSerializerTestCase

class SchoolSerializerTest(BaseSerializerTestCase):


    serializer_class = SchoolSerializer
    model = School

    @classmethod
    def setUpTestData(cls):
        cls.instance = cls.model()

        for field in cls.model._meta.fields:
            if field.primary_key:
                continue

            if field.auto_created:
                continue

            if field.auto_now or field.auto_now_add:
                continue

            if field.has_default():
                continue

            if field.null:
                continue

            if field.blank:
                continue

            if field.get_internal_type() == "CharField":
                setattr(cls.instance, field.name, "Test School")

        cls.instance.save()

    def setUp(self):
        self.instance = self.__class__.instance
