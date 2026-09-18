from django.test import TestCase

from nphs_school.models import School


class SchoolModelTest(TestCase):

    def test_create_school(self):
        school = School.objects.create(
            name="Narayanpur High School",
            location_address="Narayanpur, Chauddagram, Cumilla",
            contact_email="school@example.com",
            contact_phone="01234567890",
        )

        self.assertIsNotNone(school.pk)
        self.assertEqual(
            school.name,
            "Narayanpur High School",
        )
        self.assertEqual(
            school.location_address,
            "Narayanpur, Chauddagram, Cumilla",
        )

    def test_default_code_is_used(self):
        school = School.objects.create(
            name="Narayanpur High School",
            location_address="Narayanpur, Cumilla",
            contact_email="school@example.com",
            contact_phone="01234567890",
        )

        self.assertEqual(school.code, "105409")

    def test_custom_code(self):
        school = School.objects.create(
            name="Narayanpur High School",
            code="NHS001",
            location_address="Narayanpur, Cumilla",
            contact_email="school@example.com",
            contact_phone="01234567890",
        )

        self.assertEqual(school.code, "NHS001")

    def test_motto_is_optional(self):
        school = School.objects.create(
            name="Narayanpur High School",
            location_address="Narayanpur, Cumilla",
            contact_email="school@example.com",
            contact_phone="01234567890",
        )

        self.assertEqual(school.motto, "")

    def test_motto_can_be_set(self):
        school = School.objects.create(
            name="Narayanpur High School",
            motto="Knowledge is Power",
            location_address="Narayanpur, Cumilla",
            contact_email="school@example.com",
            contact_phone="01234567890",
        )

        self.assertEqual(
            school.motto,
            "Knowledge is Power",
        )

    def test_logo_is_optional(self):
        school = School.objects.create(
            name="Narayanpur High School",
            location_address="Narayanpur, Cumilla",
            contact_email="school@example.com",
            contact_phone="01234567890",
        )

        self.assertFalse(school.logo)

    def test_string_representation(self):
        school = School.objects.create(
            name="Narayanpur High School",
            code="NHS001",
            location_address="Narayanpur, Cumilla",
            contact_email="school@example.com",
            contact_phone="01234567890",
        )

        self.assertEqual(
            str(school),
            "Narayanpur High School (NHS001)",
        )

    def test_created_at_is_set(self):
        school = School.objects.create(
            name="Narayanpur High School",
            location_address="Narayanpur, Cumilla",
            contact_email="school@example.com",
            contact_phone="01234567890",
        )

        self.assertIsNotNone(school.created_at)

    def test_updated_at_is_set(self):
        school = School.objects.create(
            name="Narayanpur High School",
            location_address="Narayanpur, Cumilla",
            contact_email="school@example.com",
            contact_phone="01234567890",
        )

        self.assertIsNotNone(school.updated_at)

    