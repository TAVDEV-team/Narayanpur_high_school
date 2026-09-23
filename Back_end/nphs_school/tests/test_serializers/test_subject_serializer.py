from nphs_school.models import Subject
from nphs_school.serializers.subject_serializer import (
SubjectListSerializer,
SubjectSerializer,
)

from .common_serializer import BaseSerializerTestCase

class SubjectSerializerTest(BaseSerializerTestCase):


    serializer_class = SubjectSerializer

    expected_fields = [
        "id",
        "name",
        "subject_type",
        "code",
        "written_marks",
        "practical_marks",
        "mcq_marks",
        "total_marks",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(
            name="Mathematics",
            subject_type=Subject.SubjectType.COMPULSORY,
            code="MATH",
            written_marks=70,
            practical_marks=20,
            mcq_marks=10,
        )

    def setUp(self):
        self.instance = self.subject

    def test_total_marks_returns_sum_of_all_marks(self):
        serializer = self.serializer_class(self.subject)

        self.assertEqual(
            serializer.data["total_marks"],
            100,
        )

    def test_total_marks_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["total_marks"].read_only
        )

    def test_subject_fields_are_serialized_correctly(self):
        serializer = self.serializer_class(self.subject)

        self.assertEqual(
            serializer.data["name"],
            "Mathematics",
        )
        self.assertEqual(
            serializer.data["subject_type"],
            Subject.SubjectType.COMPULSORY,
        )
        self.assertEqual(
            serializer.data["code"],
            "MATH",
        )
        self.assertEqual(
            serializer.data["written_marks"],
            70,
        )
        self.assertEqual(
            serializer.data["practical_marks"],
            20,
        )
        self.assertEqual(
            serializer.data["mcq_marks"],
            10,
        )


class SubjectListSerializerTest(BaseSerializerTestCase):


    serializer_class = SubjectListSerializer

    expected_fields = [
        "id",
        "name",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(
            name="English",
            subject_type=Subject.SubjectType.COMPULSORY,
            code="ENG",
            written_marks=70,
            practical_marks=0,
            mcq_marks=30,
        )

    def setUp(self):
        self.instance = self.subject

    def test_only_id_and_name_are_serialized(self):
        serializer = self.serializer_class(self.subject)

        self.assertEqual(
            set(serializer.data.keys()),
            {"id", "name"},
        )

    def test_name_is_serialized_correctly(self):
        serializer = self.serializer_class(self.subject)

        self.assertEqual(
            serializer.data["name"],
            "English",
        )

