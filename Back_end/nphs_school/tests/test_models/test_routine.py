from django.test import TestCase

from accounts.models import Account, TeacherAccount
from nphs_school.models import AClass, Routine, Subject
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RoutineModelTest(TestCase):

    def setUp(self):
        self.academic_class = AClass.objects.create(
            name="9_science",
            room_number="201",
            grade=9,
            group="science",
        )

        self.subject = Subject.objects.create(
            name="Physics",
            code="PHY1",
            subject_type=Subject.SubjectType.GROUP,
        )

        self.user = User.objects.create(
            username="testteacher",
            first_name="Test",
            last_name="Teacher",
        )

        self.account = Account.objects.create(
            user=self.user,
            mobile="01712345678",
            date_of_birth="1990-01-01",
            joining_date="2020-01-01",
            address="Dhaka, Bangladesh",
            last_educational_institute="Dhaka University",
        )

        self.teacher = TeacherAccount.objects.create(
            account=self.account,
            base_subject=self.subject,
        )

    def test_create_routine(self):
        routine = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=self.teacher,
            slot="1",
        )

        self.assertIsNotNone(routine.pk)
        self.assertEqual(routine.aclass, self.academic_class)
        self.assertEqual(routine.day, "MON")
        self.assertEqual(routine.subject, self.subject)
        self.assertEqual(routine.teacher, self.teacher)
        self.assertEqual(routine.slot, "1")

    def test_subject_is_optional(self):
        routine = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            teacher=self.teacher,
            slot="2",
        )

        self.assertIsNone(routine.subject)

    def test_teacher_is_optional(self):
        routine = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            slot="2",
        )

        self.assertIsNone(routine.teacher)

    def test_routine_can_have_no_subject_and_no_teacher(self):
        routine = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=None,
            teacher=None,
            slot="3",
        )

        self.assertIsNone(routine.subject)
        self.assertIsNone(routine.teacher)

    def test_str_returns_expected_value(self):
        routine = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=self.teacher,
            slot="1",
        )

        expected = (
            f"{self.academic_class} - "
            f"Monday - "
            f"10:00 AM - 10:45 AM - "
            f"{self.subject}"
        )

        self.assertEqual(str(routine), expected)

    def test_same_class_day_slot_cannot_be_duplicated(self):
        Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            slot="1",
            subject=self.subject,
            teacher=self.teacher,
        )
        with self.assertRaises(ValidationError):
            Routine.objects.create(
                aclass=self.academic_class,
                day="MON",
                slot="1",
                subject=self.subject,
                teacher=self.teacher,
            )

    def test_same_teacher_day_slot_cannot_be_duplicated(self):
        Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=self.teacher,
            slot="1",
        )

        another_class = AClass.objects.create(
            name="10_science",
            room_number="202",
            grade=10,
            group="science",
        )

        with self.assertRaises(ValidationError):
            Routine.objects.create(
                aclass=another_class,
                day="MON",
                subject=self.subject,
                teacher=self.teacher,
                slot="1",
            )

    def test_same_class_can_have_different_slots(self):
        routine_1 = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=self.teacher,
            slot="1",
        )

        routine_2 = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=None,
            slot="2",
        )

        self.assertNotEqual(routine_1.pk, routine_2.pk)

    def test_same_class_can_have_same_slot_on_different_days(self):
        routine_1 = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            slot="1",
        )

        routine_2 = Routine.objects.create(
            aclass=self.academic_class,
            day="TUE",
            subject=self.subject,
            slot="1",
        )

        self.assertNotEqual(routine_1.pk, routine_2.pk)

    def test_same_teacher_can_teach_different_slots(self):
        routine_1 = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=self.teacher,
            slot="1",
        )

        routine_2 = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=self.teacher,
            slot="2",
        )

        self.assertNotEqual(routine_1.pk, routine_2.pk)

    def test_deleting_subject_sets_routine_subject_to_null(self):
        routine = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=self.teacher,
            slot="1",
        )

        self.subject.delete()

        routine.refresh_from_db()

        self.assertIsNone(routine.subject)

    def test_deleting_teacher_sets_routine_teacher_to_null(self):
        routine = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=self.teacher,
            slot="1",
        )

        self.teacher.delete()

        routine.refresh_from_db()

        self.assertIsNone(routine.teacher)

    def test_deleting_class_deletes_routine(self):
        routine = Routine.objects.create(
            aclass=self.academic_class,
            day="MON",
            subject=self.subject,
            teacher=self.teacher,
            slot="1",
        )

        routine_id = routine.pk

        self.academic_class.delete()

        self.assertFalse(Routine.objects.filter(pk=routine_id).exists())

    def test_all_days_are_defined(self):
        expected_days = {
            "MON",
            "TUE",
            "WED",
            "THU",
            "FRI",
            "SAT",
            "SUN",
        }

        actual_days = {value for value, label in Routine.DAYS_OF_WEEK}

        self.assertEqual(actual_days, expected_days)

    def test_all_slots_are_defined(self):
        expected_slots = {
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
        }

        actual_slots = {value for value, label in Routine.CLASS_SLOTS}

        self.assertEqual(actual_slots, expected_slots)
