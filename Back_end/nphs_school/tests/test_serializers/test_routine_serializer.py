from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from nphs_school.models import AClass, Routine, Subject
from accounts.models import TeacherAccount, Account
from nphs_school.serializers.routine_serializer import RoutineSerializer

from .common_serializer import BaseSerializerTestCase

class RoutineSerializerTest(BaseSerializerTestCase):


    serializer_class = RoutineSerializer
    model = Routine

    @classmethod
    def setUpTestData(cls):
        cls.aclass = AClass.objects.create(
            name="6",
            room_number="101",
        )

        cls.subject = Subject.objects.create(
            name="Mathematics",
            subject_type="compulsory",
            code="MATH",
            written_marks=70,
            practical_marks=0,
            mcq_marks=30,
        )

        user = User.objects.create_user(
            username="teacher1",
            first_name="John",
            last_name="Doe",
            password="testpass123",
        )

        account = Account.objects.create(
            user=user,
            mobile="01712345678",  # normalize_mobile handles this format
            date_of_birth="1985-01-01",
            joining_date="2020-01-01",
            address="Some address, Dhaka",
            last_educational_institute="Dhaka University",
        )

        cls.teacher = TeacherAccount.objects.create(
            account=account,
            base_subject=cls.subject,
        )

        cls.routine = Routine.objects.create(
                aclass=cls.aclass,
                day="MON",
                slot="1",
                subject=cls.subject,
                teacher=cls.teacher,
            )

    def setUp(self):
        self.instance = self.routine

        self.expected_fields = [
            "id",
            "aclass",
            "day",
            "day_display",
            "slot",
            "slot_display",
            "subject",
            "teacher",
        ]

    # def test_serializer_fields(self):
    #     self.test_serializer_contains_expected_model_fields()

    def test_day_display_returns_human_readable_day(self):
        serializer = self.serializer_class(self.routine)

        self.assertEqual(
            serializer.data["day_display"],
            "Monday",
        )

    def test_slot_display_returns_human_readable_slot(self):
        serializer = self.serializer_class(self.routine)

        self.assertEqual(
            serializer.data["slot_display"],
            "10:00 AM - 10:45 AM",
        )

    def test_day_display_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["day_display"].read_only
        )

    def test_slot_display_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["slot_display"].read_only
        )

    def test_day_is_serialized_correctly(self):
        serializer = self.serializer_class(self.routine)

        self.assertEqual(
            serializer.data["day"],
            "MON",
        )

    def test_slot_is_serialized_correctly(self):
        serializer = self.serializer_class(self.routine)

        self.assertEqual(
            serializer.data["slot"],
            "1",
        )
