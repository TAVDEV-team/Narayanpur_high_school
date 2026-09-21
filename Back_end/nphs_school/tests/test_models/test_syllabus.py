from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase

from nphs_school.models import AClass, Syllabus


class SyllabusModelTest(TestCase):

    def create_test_file(self):
        return SimpleUploadedFile(
            "syllabus.pdf",
            b"fake syllabus content",
            content_type="application/pdf",
        )

    def create_class(self):
        return AClass.objects.create(
            name="9_science",
            room_number="201",
            grade=9,
            group="science",
        )

    def test_create_syllabus(self):
        academic_class = self.create_class()

        syllabus = Syllabus.objects.create(
            title="Class 9 Science Syllabus",
            aclass=academic_class,
            file=self.create_test_file(),
        )

        self.assertIsNotNone(syllabus.pk)
        self.assertEqual(
            syllabus.title,
            "Class 9 Science Syllabus"
        )
        self.assertEqual(syllabus.aclass, academic_class)
        self.assertTrue(syllabus.file)

    def test_str_returns_title(self):
        syllabus = Syllabus.objects.create(
            title="Physics Syllabus",
            file=self.create_test_file(),
        )

        self.assertEqual(str(syllabus), "Physics Syllabus")

    def test_aclass_is_optional(self):
        syllabus = Syllabus.objects.create(
            title="General Syllabus",
            file=self.create_test_file(),
        )

        self.assertIsNone(syllabus.aclass)

    def test_uploaded_at_is_set(self):
        syllabus = Syllabus.objects.create(
            title="Mathematics Syllabus",
            file=self.create_test_file(),
        )

        self.assertIsNotNone(syllabus.uploaded_at)

    def test_file_is_saved(self):
        syllabus = Syllabus.objects.create(
            title="English Syllabus",
            file=self.create_test_file(),
        )

        self.assertTrue(syllabus.file.name)
        self.assertFalse(
            syllabus.file.name.endswith("syllabus.pdf")
        )

    def test_one_class_can_have_only_one_syllabus(self):
        academic_class = self.create_class()

        Syllabus.objects.create(
            title="First Syllabus",
            aclass=academic_class,
            file=self.create_test_file(),
        )

        with self.assertRaises(IntegrityError):
            Syllabus.objects.create(
                title="Second Syllabus",
                aclass=academic_class,
                file=self.create_test_file(),
            )

    def test_different_classes_can_have_different_syllabuses(self):
        class_one = self.create_class()

        class_two = AClass.objects.create(
            name="10_science",
            room_number="202",
            grade=10,
            group="science",
        )

        syllabus_one = Syllabus.objects.create(
            title="Class 9 Syllabus",
            aclass=class_one,
            file=self.create_test_file(),
        )

        syllabus_two = Syllabus.objects.create(
            title="Class 10 Syllabus",
            aclass=class_two,
            file=self.create_test_file(),
        )

        self.assertNotEqual(syllabus_one.pk, syllabus_two.pk)

    def test_deleting_class_sets_syllabus_class_to_null(self):
        academic_class = self.create_class()

        syllabus = Syllabus.objects.create(
            title="Science Syllabus",
            aclass=academic_class,
            file=self.create_test_file(),
        )

        academic_class.delete()

        syllabus.refresh_from_db()

        self.assertIsNone(syllabus.aclass)

    def test_syllabus_can_exist_without_class(self):
        syllabus = Syllabus.objects.create(
            title="General School Syllabus",
            aclass=None,
            file=self.create_test_file(),
        )

        self.assertIsNone(syllabus.aclass)
        self.assertTrue(syllabus.file)