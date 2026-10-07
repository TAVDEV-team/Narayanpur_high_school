from nphs_school.models import AClass, Subject
from nphs_school.serializers.aclass_serializer import (
AClassMetaSerializer,
AClassReadSerializer,
AClassSerializer,
AClassSubjectSerializer,
)

from .common_serializer import BaseSerializerTestCase

class AClassReadSerializerTest(BaseSerializerTestCase):


    serializer_class = AClassReadSerializer

    expected_fields = [
        "id",
        "name",
        "room_number",
        "students",
        "all_subjects",
        "created_at",
        "updated_at",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.aclass = AClass.objects.create(
            name="6",
            room_number="101",
        )

        cls.subject = Subject.objects.create(
            name="Mathematics",
            subject_type=Subject.SubjectType.COMPULSORY,
            code="MATH",
            written_marks=70,
            practical_marks=0,
            mcq_marks=30,
        )

        cls.aclass.compulsory.add(cls.subject)

    def setUp(self):
        self.instance = self.aclass

    def test_students_returns_empty_list_when_no_students_exist(self):
        serializer = self.serializer_class(self.aclass)

        self.assertEqual(
            serializer.data["students"],
            [],
        )

    def test_all_subjects_returns_class_subjects(self):
        serializer = self.serializer_class(self.aclass)

        self.assertEqual(
            len(serializer.data["all_subjects"]),
            1,
        )

        self.assertEqual(
            serializer.data["all_subjects"][0]["id"],
            self.subject.id,
        )

        self.assertEqual(
            serializer.data["all_subjects"][0]["name"],
            "Mathematics",
        )

    def test_all_fields_are_read_only(self):
        serializer = self.serializer_class()

        for field_name in self.expected_fields:
            self.assertTrue(
                serializer.fields[field_name].read_only
            )


class AClassSerializerTest(BaseSerializerTestCase):


    serializer_class = AClassSerializer

    expected_fields = [
        "id",
        "name",
        "all_subjects",
        "created_at",
        "updated_at",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.aclass = AClass.objects.create(
            name="7",
            room_number="102",
        )

        cls.subject = Subject.objects.create(
            name="English",
            subject_type=Subject.SubjectType.COMPULSORY,
            code="ENG",
            written_marks=70,
            practical_marks=0,
            mcq_marks=30,
        )

        cls.aclass.compulsory.add(cls.subject)

    def setUp(self):
        self.instance = self.aclass

    def test_all_subjects_returns_nested_subjects(self):
        serializer = self.serializer_class(self.aclass)

        self.assertEqual(
            serializer.data["all_subjects"],
            [
                {
                    "id": self.subject.id,
                    "name": "English",
                }
            ],
        )

    def test_all_subjects_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["all_subjects"].read_only
        )

    def test_created_at_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["created_at"].read_only
        )

    def test_updated_at_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["updated_at"].read_only
        )


class AClassMetaSerializerTest(BaseSerializerTestCase):


    serializer_class = AClassMetaSerializer

    expected_fields = [
        "id",
        "name",
        "room_number",
        "total_students",
        "male_students",
        "female_students",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.aclass = AClass.objects.create(
            name="8",
            room_number="103",
        )

    def setUp(self):
        self.instance = self.aclass

    def test_total_students_returns_zero_without_students(self):
        serializer = self.serializer_class(self.aclass)

        self.assertEqual(
            serializer.data["total_students"],
            0,
        )

    def test_male_students_returns_zero_without_students(self):
        serializer = self.serializer_class(self.aclass)

        self.assertEqual(
            serializer.data["male_students"],
            0,
        )

    def test_female_students_returns_zero_without_students(self):
        serializer = self.serializer_class(self.aclass)

        self.assertEqual(
            serializer.data["female_students"],
            0,
        )


class AClassSubjectSerializerTest(BaseSerializerTestCase):


    serializer_class = AClassSubjectSerializer

    expected_fields = [
        "all_subjects",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.aclass = AClass.objects.create(
            name="9_science",
            room_number="104",
        )

        cls.subject = Subject.objects.create(
            name="Physics",
            subject_type=Subject.SubjectType.GROUP,
            code="PHY",
            written_marks=70,
            practical_marks=20,
            mcq_marks=10,
        )

        cls.aclass.group_subjects.add(cls.subject)

    def setUp(self):
        self.instance = self.aclass

    def test_all_subjects_returns_nested_subjects(self):
        serializer = self.serializer_class(self.aclass)

        self.assertEqual(
            serializer.data["all_subjects"],
            [
                {
                    "id": self.subject.id,
                    "name": "Physics",
                }
            ],
        )

    def test_all_subjects_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["all_subjects"].read_only
        )
