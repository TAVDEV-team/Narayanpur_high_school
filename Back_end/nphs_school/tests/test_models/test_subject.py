from django.core.exceptions import ValidationError
from django.test import TestCase

from nphs_school.models import Subject


class SubjectModelTest(TestCase):

    def test_create_subject(self):
        subject = Subject.objects.create(
            name="Mathematics",
            code="MATH",
        )

        self.assertIsNotNone(subject.pk)
        self.assertEqual(subject.subject_type, Subject.SubjectType.COMPULSORY)
        self.assertEqual(subject.written_marks, 0)
        self.assertEqual(subject.practical_marks, 0)
        self.assertEqual(subject.mcq_marks, 0)

    def test_total_marks(self):
        subject = Subject(
            name="Physics",
            code="PHY1",
            written_marks=50,
            practical_marks=25,
            mcq_marks=25,
        )

        self.assertEqual(subject.total_marks, 100)

    def test_total_marks_with_zero_values(self):
        subject = Subject(
            name="History",
            code="HIST",
        )

        self.assertEqual(subject.total_marks, 0)

    def test_total_marks_cannot_exceed_100(self):
        subject = Subject(
            name="Chemistry",
            code="CHEM",
            written_marks=60,
            practical_marks=25,
            mcq_marks=25,
        )

        with self.assertRaises(ValidationError) as context:
            subject.full_clean()

        self.assertIn("Total marks cannot exceed 100.", str(context.exception))

    def test_total_marks_equal_to_100_is_valid(self):
        subject = Subject(
            name="Biology",
            code="BIO1",
            written_marks=50,
            practical_marks=25,
            mcq_marks=25,
        )

        subject.full_clean()

    def test_subject_name_must_be_unique(self):
        Subject.objects.create(
            name="English",
            code="ENG1",
        )

        duplicate = Subject(
            name="English",
            code="ENG2",
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_subject_code_must_be_unique(self):
        Subject.objects.create(
            name="Bangla",
            code="BAN1",
        )

        duplicate = Subject(
            name="Another Bangla",
            code="BAN1",
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_subject_name_max_length(self):
        subject = Subject(
            name="A" * 121,
            code="SUB1",
        )

        with self.assertRaises(ValidationError):
            subject.full_clean()

    def test_subject_code_max_length(self):
        subject = Subject(
            name="Computer Science",
            code="ABCDE",
        )

        with self.assertRaises(ValidationError):
            subject.full_clean()

    def test_all_subject_types_are_available(self):
        expected_types = {
            "compulsory",
            "religious",
            "group",
            "group_optional",
            "optional",
            "extra",
        }

        actual_types = {value for value, label in Subject.SubjectType.choices}

        self.assertEqual(actual_types, expected_types)

    def test_str_returns_name_and_code(self):
        subject = Subject.objects.create(
            name="Physics",
            code="PHY1",
        )

        self.assertEqual(str(subject), "Physics - PHY1")
