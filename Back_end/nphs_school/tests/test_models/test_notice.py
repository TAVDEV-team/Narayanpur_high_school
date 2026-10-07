from datetime import date

from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from nphs_school.models import Notice
from accounts.models import TeacherAccount, HeadMasterAccount, Account
from nphs_school.models import Subject

User = get_user_model()


class NoticeModelTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(
            name="General Studies",
            code="GS01",
            written_marks=70,
            practical_marks=0,
            mcq_marks=30,
        )

        # --- Headmaster user ---
        self.headmaster_user = User.objects.create_user(
            username="headmaster",
            password="testpass123",
            first_name="Head",
            last_name="Master",
        )
        headmaster_account = Account.objects.create(
            user=self.headmaster_user,
            mobile="01712345678",
            date_of_birth=date(1980, 1, 1),
            joining_date=date(2015, 1, 1),
            address="Test Address",
            last_educational_institute="Test University",
        )
        headmaster_teacher = TeacherAccount.objects.create(
            account=headmaster_account,
            base_subject=self.subject,
        )
        HeadMasterAccount.objects.create(
            teacher=headmaster_teacher,
            appointed_date=date(2020, 1, 1),
        )

        # --- Non-headmaster user (a regular teacher) ---
        self.other_user = User.objects.create_user(
            username="regular_teacher",
            password="testpass123",
            first_name="Regular",
            last_name="Teacher",
        )
        other_account = Account.objects.create(
            user=self.other_user,
            mobile="01812345678",
            date_of_birth=date(1985, 1, 1),
            joining_date=date(2018, 1, 1),
            address="Test Address",
            last_educational_institute="Test University",
        )
        TeacherAccount.objects.create(
            account=other_account,
            base_subject=self.subject,
        )

    def create_notice(
        self,
        title="School Notice",
        description="This is a test notice.",
        notice_for_date=None,
        is_active=True,
    ):
        if notice_for_date is None:
            notice_for_date = date.today()

        return Notice.objects.create(
            title=title,
            description=description,
            notice_for_date=notice_for_date,
            is_active=is_active,
        )

    def test_create_notice(self):
        notice = self.create_notice()

        self.assertIsNotNone(notice.pk)
        self.assertEqual(notice.title, "School Notice")
        self.assertEqual(
            notice.description,
            "This is a test notice.",
        )

    def test_default_is_active_is_true(self):
        notice = self.create_notice()

        self.assertTrue(notice.is_active)

    def test_default_notice_for_date_is_today(self):
        notice = Notice.objects.create(
            title="Today's Notice",
            description="Notice description.",
        )

        self.assertEqual(
            notice.notice_for_date,
            date.today(),
        )

    def test_short_description_for_short_text(self):
        description = "This is a short description."

        notice = self.create_notice(
            description=description,
        )

        self.assertEqual(
            notice.short_description,
            description,
        )

    def test_short_description_for_long_text(self):
        description = "A" * 100

        notice = self.create_notice(
            description=description,
        )

        self.assertEqual(
            notice.short_description,
            "A" * 50 + "...",
        )

    def test_short_description_is_read_only(self):
        notice = self.create_notice()

        with self.assertRaises(AttributeError):
            notice.short_description = "New description"

    def test_is_approved_returns_false_by_default(self):
        notice = self.create_notice()

        self.assertFalse(notice.is_approved())

    def test_is_approved_returns_true_after_approval(self):
        notice = self.create_notice()

        notice.approved_by_headmaster = True

        self.assertTrue(notice.is_approved())

    def test_approve_marks_notice_as_approved(self):
        notice = self.create_notice()
        approved = notice.approve(self.headmaster_user)
        notice.refresh_from_db()

        self.assertTrue(approved)
        self.assertTrue(notice.approved_by_headmaster)

    def test_approve_sets_approved_at(self):
        notice = self.create_notice()
        notice.approve(self.headmaster_user)
        notice.refresh_from_db()

        self.assertIsNotNone(
            notice.approved_at
        )  # note: was assertIsNone before — that was testing the old bug

    def test_approve_rejects_non_headmaster(self):
        notice = self.create_notice()

        with self.assertRaises(PermissionDenied):
            notice.approve(self.other_user)

        notice.refresh_from_db()
        self.assertFalse(notice.approved_by_headmaster)

    def test_approve_is_idempotent(self):
        notice = self.create_notice()
        notice.approve(self.headmaster_user)

        result = notice.approve(self.headmaster_user)  # second call

        self.assertFalse(result)  # returns False, doesn't re-approve or error

    def test_slug_is_generated_automatically(self):
        notice = self.create_notice(
            title="Annual Sports Day 2026",
        )

        self.assertEqual(
            notice.slug,
            "annual-sports-day-2026",
        )

    def test_slug_is_unique(self):
        first_notice = self.create_notice(
            title="Admission Notice",
            notice_for_date=date(2026, 9, 18),
        )

        second_notice = self.create_notice(
            title="Admission Notice",
            notice_for_date=date(2026, 9, 19),
        )

        self.assertEqual(
            first_notice.slug,
            "admission-notice",
        )

        self.assertEqual(
            second_notice.slug,
            "admission-notice-1",
        )

    def test_slug_gets_incremented_for_multiple_duplicates(self):
        notice_1 = self.create_notice(
            title="Exam Notice",
            notice_for_date=date(2026, 9, 18),
        )

        notice_2 = self.create_notice(
            title="Exam Notice",
            notice_for_date=date(2026, 9, 19),
        )

        notice_3 = self.create_notice(
            title="Exam Notice",
            notice_for_date=date(2026, 9, 20),
        )

        self.assertEqual(notice_1.slug, "exam-notice")
        self.assertEqual(notice_2.slug, "exam-notice-1")
        self.assertEqual(notice_3.slug, "exam-notice-2")

    def test_slug_does_not_change_on_update(self):
        notice = self.create_notice(
            title="Original Notice",
        )

        original_slug = notice.slug

        notice.title = "Updated Notice"
        notice.save()

        notice.refresh_from_db()

        self.assertEqual(notice.slug, original_slug)

    def test_same_title_and_date_is_not_allowed(self):
        notice_date = date(2026, 9, 18)

        self.create_notice(
            title="Holiday Notice",
            notice_for_date=notice_date,
        )

        with self.assertRaises(IntegrityError):
            Notice.objects.create(
                title="Holiday Notice",
                description="Another notice.",
                notice_for_date=notice_date,
            )

    def test_same_title_on_different_dates_is_allowed(self):
        notice_1 = self.create_notice(
            title="Holiday Notice",
            notice_for_date=date(2026, 9, 18),
        )

        notice_2 = self.create_notice(
            title="Holiday Notice",
            notice_for_date=date(2026, 9, 19),
        )

        self.assertNotEqual(notice_1.pk, notice_2.pk)

    def test_different_titles_on_same_date_are_allowed(self):
        notice_date = date(2026, 9, 18)

        notice_1 = self.create_notice(
            title="Holiday Notice",
            notice_for_date=notice_date,
        )

        notice_2 = self.create_notice(
            title="Exam Notice",
            notice_for_date=notice_date,
        )

        self.assertNotEqual(notice_1.pk, notice_2.pk)

    def test_str_returns_title_and_date(self):
        notice = self.create_notice(
            title="School Holiday",
            notice_for_date=date(2026, 9, 18),
        )

        self.assertEqual(
            str(notice),
            "School Holiday (2026-09-18)",
        )

    def test_created_at_is_set(self):
        notice = self.create_notice()

        self.assertIsNotNone(notice.created_at)

    def test_updated_at_is_set(self):
        notice = self.create_notice()

        self.assertIsNotNone(notice.updated_at)

    def test_inactive_notice_can_be_created(self):
        notice = self.create_notice(
            is_active=False,
        )

        self.assertFalse(notice.is_active)

    def test_notice_ordering(self):
        older_notice = self.create_notice(
            title="Older Notice",
            notice_for_date=date(2026, 9, 10),
        )

        newer_notice = self.create_notice(
            title="Newer Notice",
            notice_for_date=date(2026, 9, 18),
        )

        notices = list(Notice.objects.all())

        self.assertEqual(notices[0], newer_notice)
        self.assertEqual(notices[1], older_notice)
