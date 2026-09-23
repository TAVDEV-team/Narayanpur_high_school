from datetime import date

from django.contrib.auth.models import User

from accounts.models import Account, TeacherAccount
from nphs_school.models import Messages, Subject
from nphs_school.serializers.message_serializer import (
MessageTeacherSerializer,
MessagesSerializer,
)
from .common_serializer import BaseSerializerTestCase

class MessageTeacherSerializerTest(BaseSerializerTestCase):


    serializer_class = MessageTeacherSerializer

    expected_fields = [
        "image",
        "full_name",
    ]

    @classmethod
    def setUpTestData(cls):

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
                            mobile="01712345678",  
                            date_of_birth="1985-01-01",
                            joining_date="2020-01-01",
                            address="Some address, Dhaka",
                            last_educational_institute="Dhaka University",
                        )
                
        cls.teacher = TeacherAccount.objects.create(
                                    account=account,
                                    base_subject=cls.subject,
                                )
                       
            
    def setUp(self):
        self.instance = self.teacher

    def test_full_name_returns_account_full_name(self):
        serializer = self.serializer_class(self.teacher)

        self.assertEqual(
            serializer.data["full_name"],
            "John Doe",
        )

    def test_full_name_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["full_name"].read_only
        )

    def test_image_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["image"].read_only
        )


class MessagesSerializerTest(BaseSerializerTestCase):

    serializer_class = MessagesSerializer

    expected_fields = [
        "id",
        "message",
        "created_at",
        "updated_at",
        "message_of",
    ]

    @classmethod
    def setUpTestData(cls):
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
                            first_name="Karim",
                            last_name="Hasan",
                            password="testpass123",
                        )        
        
        account = Account.objects.create(
                            user=user,
                            mobile="01712345678",  
                            date_of_birth="1985-01-01",
                            joining_date="2020-01-01",
                            address="Some address, Dhaka",
                            last_educational_institute="Dhaka University",
                        )

        cls.teacher = TeacherAccount.objects.create(
                                    account=account,
                                    base_subject=cls.subject,
                                )       
                        
                
        
        cls.message = Messages.objects.create(
            message_of=cls.teacher,
            message="Welcome to our school.",
        )

    def setUp(self):
        self.instance = self.message

    def test_message_is_serialized_correctly(self):
        serializer = self.serializer_class(self.message)

        self.assertEqual(
            serializer.data["message"],
            "Welcome to our school.",
        )

    def test_message_of_is_nested(self):
        serializer = self.serializer_class(self.message)

        self.assertEqual(
            serializer.data["message_of"]["full_name"],
            "Karim Hasan",
        )

    def test_message_of_contains_teacher_information(self):
        serializer = self.serializer_class(self.message)

        self.assertIn(
            "full_name",
            serializer.data["message_of"],
        )

        self.assertIn(
            "image",
            serializer.data["message_of"],
        )

    def test_message_of_is_read_only(self):
        serializer = self.serializer_class()

        self.assertTrue(
            serializer.fields["message_of"].read_only
        )

    def test_created_at_is_serialized(self):
        serializer = self.serializer_class(self.message)

        self.assertIsNotNone(
            serializer.data["created_at"]
        )

    def test_updated_at_is_serialized(self):
        serializer = self.serializer_class(self.message)

        self.assertIsNotNone(
            serializer.data["updated_at"]
        )


