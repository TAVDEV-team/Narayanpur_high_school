from nphs_school.models import Batch
from nphs_school.serializers.batch_serializer import BatchSerializer

from .common_serializer import BaseSerializerTestCase

class BatchSerializerTest(BaseSerializerTestCase):


    serializer_class = BatchSerializer
    model = Batch

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

            if field.null or field.blank:
                continue

            if field.get_internal_type() == "CharField":
                setattr(cls.instance, field.name, "Test Batch")

        cls.instance.save()

    def setUp(self):
        self.instance = self.__class__.instance
