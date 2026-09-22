from django.core.exceptions import ValidationError
from django.test import TestCase

from nphs_school.models import AClass, Subject


class AClassModelTest(TestCase):

    def create_subject(
        self,
        name,
        code,
        subject_type=Subject.SubjectType.COMPULSORY,
    ):
        return Subject.objects.create(
            name=name,
            code=code,
            subject_type=subject_type,
        )

    def test_create_academic_class(self):
        academic_class = AClass.objects.create(
            name="6",
            room_number="101",
        )

        self.assertIsNotNone(academic_class.pk)
        self.assertEqual(academic_class.name, "6")
        self.assertEqual(academic_class.room_number, "101")
        self.assertEqual(academic_class.grade, 0)
        self.assertIsNone(academic_class.group)

    def test_str_returns_display_name(self):
        academic_class = AClass.objects.create(
            name="6",
            room_number="101",
        )

        self.assertEqual(str(academic_class), "Class 6")

    def test_str_returns_science_display_name(self):
        academic_class = AClass.objects.create(
            name="9_science",
            room_number="201",
        )

        self.assertEqual(str(academic_class), "Class 9 Science")

    def test_class_name_must_be_unique(self):
        AClass.objects.create(
            name="7",
            room_number="102",
        )

        duplicate = AClass(
            name="7",
            room_number="103",
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_all_subjects_returns_all_subject_categories(self):
        academic_class = AClass.objects.create(
            name="9_science",
            room_number="201",
            grade=9,
        )

        compulsory = self.create_subject(
            "Bangla",
            "BAN1",
            Subject.SubjectType.COMPULSORY,
        )

        group_subject = self.create_subject(
            "Physics",
            "PHY1",
            Subject.SubjectType.GROUP,
        )

        religious = self.create_subject(
            "Religion",
            "REL1",
            Subject.SubjectType.RELIGIOUS,
        )

        extra = self.create_subject(
            "Computer",
            "COM1",
            Subject.SubjectType.EXTRA,
        )

        academic_class.compulsory.add(compulsory)
        academic_class.group_subjects.add(group_subject)
        academic_class.religious.add(religious)
        academic_class.extra.add(extra)

        all_subjects = academic_class.all_subjects

        self.assertEqual(len(all_subjects), 4)
        self.assertIn(compulsory, all_subjects)
        self.assertIn(group_subject, all_subjects)
        self.assertIn(religious, all_subjects)
        self.assertIn(extra, all_subjects)

    def test_group_not_allowed_for_grade_below_9(self):
        academic_class = AClass.objects.create(
            name="8",
            room_number="103",
            grade=9,
        )
        academic_class.grade = 8
        academic_class.group = "science"

        with self.assertRaises(ValidationError) as context:
            academic_class.full_clean()

        self.assertIn(
            "Groups are only allowed for grade 9 and above.",
            str(context.exception),
        )

    def test_group_allowed_for_grade_9(self):
        academic_class = AClass(
            name="9_science",
            room_number="201",
            grade=9,
            group="science",
        )

        academic_class.full_clean()

    def test_invalid_compulsory_subject_is_rejected(self):
        academic_class = AClass.objects.create(
            name="6",
            room_number="101",
            grade=6,
        )

        optional_subject = self.create_subject(
            "Optional Subject",
            "OPT1",
            Subject.SubjectType.OPTIONAL,
        )

        academic_class.compulsory.add(optional_subject)

        with self.assertRaises(ValidationError) as context:
            academic_class.full_clean()

        self.assertIn("compulsory", context.exception.message_dict)

    def test_valid_compulsory_subject_is_allowed(self):
        academic_class = AClass.objects.create(
            name="6",
            room_number="101",
            grade=6,
        )

        compulsory = self.create_subject(
            "Mathematics",
            "MAT1",
            Subject.SubjectType.COMPULSORY,
        )

        academic_class.compulsory.add(compulsory)

        academic_class.full_clean()

    def test_invalid_group_subject_is_rejected(self):
        academic_class = AClass.objects.create(
            name="9_science",
            room_number="201",
            grade=9,
            group="science",
        )

        compulsory = self.create_subject(
            "English",
            "ENG1",
            Subject.SubjectType.COMPULSORY,
        )

        academic_class.group_subjects.add(compulsory)

        with self.assertRaises(ValidationError) as context:
            academic_class.full_clean()

        self.assertIn("group_subjects", context.exception.message_dict)

    def test_group_optional_subject_is_allowed(self):
        academic_class = AClass.objects.create(
            name="9_science",
            room_number="201",
            grade=9,
            group="science",
        )

        group_optional = self.create_subject(
            "Higher Math",
            "HMTH",
            Subject.SubjectType.GROUP_OPTIONAL,
        )

        academic_class.group_subjects.add(group_optional)

        academic_class.full_clean()

    def test_invalid_religious_subject_is_rejected(self):
        academic_class = AClass.objects.create(
            name="6",
            room_number="101",
            grade=6,
        )

        compulsory = self.create_subject(
            "Bangla",
            "BAN1",
            Subject.SubjectType.COMPULSORY,
        )

        academic_class.religious.add(compulsory)

        with self.assertRaises(ValidationError) as context:
            academic_class.full_clean()

        self.assertIn("religious", context.exception.message_dict)

    def test_valid_religious_subject_is_allowed(self):
        academic_class = AClass.objects.create(
            name="6",
            room_number="101",
            grade=6,
        )

        religious = self.create_subject(
            "Islamic Studies",
            "REL1",
            Subject.SubjectType.RELIGIOUS,
        )

        academic_class.religious.add(religious)

        academic_class.full_clean()

    def test_invalid_extra_subject_is_rejected(self):
        academic_class = AClass.objects.create(
            name="6",
            room_number="101",
            grade=6,
        )

        compulsory = self.create_subject(
            "Bangla",
            "BAN1",
            Subject.SubjectType.COMPULSORY,
        )

        academic_class.extra.add(compulsory)

        with self.assertRaises(ValidationError) as context:
            academic_class.full_clean()

        self.assertIn("extra", context.exception.message_dict)

    def test_valid_extra_subject_is_allowed(self):
        academic_class = AClass.objects.create(
            name="6",
            room_number="101",
            grade=6,
        )

        extra = self.create_subject(
            "Programming",
            "PROG",
            Subject.SubjectType.EXTRA,
        )

        academic_class.extra.add(extra)

        academic_class.full_clean()
