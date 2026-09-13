
from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account
from accounts.models.account_roles import AccountRole
from accounts.models.teacher import TeacherAccount, HeadMasterAccount
from fund.models import Fund, FundTransaction
from nphs_school.models import Subject


class FundViewSetTest(APITestCase):

    def setUp(self):
        # Create subject
        self.subject = Subject.objects.create(
            name="Test Mathematics",
            code="TM01",
        )

        # Create Django user
        self.user = User.objects.create_user(
            username="headmaster",
            password="testpassword123",
            first_name="Test",
            last_name="Headmaster",
        )

        # Create Account
        self.account = Account.objects.create(
            user=self.user,
            mobile="01712345678",
            date_of_birth=date(1980, 1, 1),
            joining_date=date(2010, 1, 1),
            address="Test Address",
            last_educational_institute="Test University",
            role=AccountRole.HEADMASTER,
        )

        # Create TeacherAccount
        self.teacher = TeacherAccount.objects.create(
            account=self.account,
            base_subject=self.subject,
        )

        # Create HeadMasterAccount
        self.headmaster = HeadMasterAccount.objects.create(
            teacher=self.teacher,
            appointed_date=date(2020, 1, 1),
        )

        # Authenticate as actual headmaster
        self.client.force_authenticate(user=self.user)

        # Create/get singleton fund
        self.fund = Fund.get_solo()

    def test_get_fund_list(self):
        url = reverse("fund-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_get_fund_detail(self):
        url = reverse(
            "fund-detail",
            args=[self.fund.pk],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_fund_transaction_list(self):
        url = reverse("transactions-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_fund_transaction(self):
        url = reverse("transactions-list")

        data = {
            "fund": self.fund.pk,
            "type": "INCOME",
            "amount": 1000,
            "reason": "Donation",
            "payment_method": "Cash",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            FundTransaction.objects.count(),
            1,
        )

    def test_update_transaction_is_not_allowed(self):
        transaction = FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )

        url = reverse(
            "transactions-detail",
            args=[transaction.pk],
        )

        data = {
            "amount": 2000,
        }

        response = self.client.put(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_patch_transaction_is_not_allowed(self):
        transaction = FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )

        url = reverse(
            "transactions-detail",
            args=[transaction.pk],
        )

        data = {
            "amount": 2000,
        }

        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_delete_transaction_is_not_allowed(self):
        transaction = FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )

        url = reverse(
            "transactions-detail",
            args=[transaction.pk],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
