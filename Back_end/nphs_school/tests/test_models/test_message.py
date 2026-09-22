from django.test import TestCase

from nphs_school.models import Messages
from accounts.models import Account, TeacherAccount
from django.contrib.auth.models import User
from nphs_school.models import Subject


class MessagesModelTest(TestCase):

    def create_teacher(self):
        """
        Create a valid TeacherAccount.

        Replace the fields below with the required fields
        from your actual TeacherAccount model.
        """

    def setUp(self):

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

    def test_create_message(self):
        message = Messages.objects.create(
            message_of=self.teacher,
            message="Welcome to Narayanpur High School.",
        )

        self.assertIsNotNone(message.pk)
        self.assertEqual(message.message_of, self.teacher)
        self.assertEqual(
            message.message,
            "Welcome to Narayanpur High School.",
        )

    def test_message_can_contain_600_characters(self):
        message_text = "A" * 600

        message = Messages.objects.create(
            message_of=self.teacher,
            message=message_text,
        )

        self.assertEqual(len(message.message), 600)


def test_created_at_is_set(self):
    message = Messages.objects.create(
        message_of=self.teacher,
        message="Test message",
    )

    self.assertIsNotNone(message.created_at)


def test_updated_at_is_set(self):
    message = Messages.objects.create(
        message_of=self.teacher,
        message="Test message",
    )

    self.assertIsNotNone(message.updated_at)


def test_teacher_deletion_deletes_messages(self):
    message = Messages.objects.create(
        message_of=self.teacher,
        message="Important school announcement.",
    )

    message_id = message.pk

    self.teacher.delete()

    self.assertFalse(Messages.objects.filter(pk=message_id).exists())
