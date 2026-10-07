from datetime import date

from django.test import TestCase

from nphs_school.models import About

from django.db import transaction


class AboutModelTest(TestCase):

    def test_create_about(self):
        about = About.objects.create(
            history="The school was established to provide quality education."
        )

        self.assertIsNotNone(about.pk)
        self.assertEqual(about.name, " High School")
        self.assertEqual(about.eiin, "105000")
        self.assertEqual(about.established_at, date(1980, 1, 1))
        self.assertEqual(about.social_links, {})
        self.assertEqual(about.extra, {})

    def test_str_returns_name(self):
        about = About.objects.create(
            name="Narayanpur High School", history="School history"
        )

        self.assertEqual(str(about), "Narayanpur High School")

    def test_optional_fields_can_be_empty(self):
        about = About.objects.create(history="School history")

        self.assertIsNone(about.motto)
        self.assertFalse(about.logo)
        self.assertFalse(about.favicon)

    def test_social_links_can_store_json(self):
        about = About.objects.create(
            history="School history",
            social_links={
                "facebook": "https://facebook.com/example",
                "youtube": "https://youtube.com/example",
            },
        )

        about.refresh_from_db()

        self.assertEqual(
            about.social_links["facebook"], "https://facebook.com/example"
        )
        self.assertEqual(
            about.social_links["youtube"], "https://youtube.com/example"
        )

    def test_extra_can_store_json(self):
        about = About.objects.create(
            history="School history",
            extra={
                "contact_email": "school@example.com",
                "theme": "dark",
            },
        )

        about.refresh_from_db()

        self.assertEqual(about.extra["theme"], "dark")
        self.assertEqual(about.extra["contact_email"], "school@example.com")

    def test_created_at_and_updated_at_are_set(self):
        about = About.objects.create(history="School history")

        self.assertIsNotNone(about.created_at)
        self.assertIsNotNone(about.updated_at)

    def test_about_is_singleton(self):
        About.objects.create(history="First school history")

        self.assertEqual(About.objects.count(), 1)

        with self.assertRaises(Exception):
            with transaction.atomic():
                About.objects.create(history="Second school history")

        self.assertEqual(About.objects.count(), 1)
