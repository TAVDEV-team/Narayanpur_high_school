from django.core.files.uploadedfile import SimpleUploadedFile

from nphs_school.models import AClass, Syllabus
from nphs_school.serializers.syllabus_serializer import SyllabusSerializer

from .common_serializer import BaseSerializerTestCase

class SyllabusSerializerTest(BaseSerializerTestCase):


    serializer_class = SyllabusSerializer

    expected_fields = [
        "id",
        "aclass",
        "class_title",
        "title",
        "file",
        "uploaded_at",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.aclass = AClass.objects.create(
            name="6",
            room_number="101",
        )

        syllabus_file = SimpleUploadedFile(
            "syllabus.pdf",
            b"fake pdf content",
            content_type="application/pdf",
        )

        cls.syllabus = Syllabus.objects.create(
            title="Class 6 Mathematics Syllabus",
            aclass=cls.aclass,
            file=syllabus_file,
        )

    def setUp(self):
        self.instance = self.syllabus

    def test_class_title_returns_aclass_name(self):
        serializer = self.serializer_class(self.syllabus)

        self.assertEqual(
            serializer.data["class_title"],
            self.aclass.name,
        )

    def test_class_title_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["class_title"].read_only
        )

    def test_aclass_returns_primary_key(self):
        serializer = self.serializer_class(self.syllabus)

        self.assertEqual(
            serializer.data["aclass"],
            self.aclass.pk,
        )

    def test_title_is_serialized_correctly(self):
        serializer = self.serializer_class(self.syllabus)

        self.assertEqual(
            serializer.data["title"],
            "Class 6 Mathematics Syllabus",
        )

    def test_uploaded_at_is_serialized(self):
        serializer = self.serializer_class(self.syllabus)

        self.assertIsNotNone(
            serializer.data["uploaded_at"]
        )
