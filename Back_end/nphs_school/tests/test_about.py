from django.test import TestCase
from nphs_school.models import About
from datetime import date

class AboutModelTest(TestCase):
    def test_about_defaults(self):
        about = About.get_solo()
        self.assertEqual(about.name, "Naraynpur High School")
        self.assertEqual(about.eiin, "105409")
        self.assertEqual(about.established_at, date(1980, 1, 1))