from nphs_school.models import Notice
from nphs_school.serializers.notice_serializer import NoticeSerializer

from .common_serializer import BaseSerializerTestCase

class NoticeSerializerTest(BaseSerializerTestCase):


    serializer_class = NoticeSerializer
    model = Notice

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
                setattr(cls.instance, field.name, "Test Notice")

        cls.instance.save()

    def setUp(self):
        self.instance = self.__class__.instance
