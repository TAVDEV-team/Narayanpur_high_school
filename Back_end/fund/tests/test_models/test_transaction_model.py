from django.core.exceptions import ValidationError
from django.test import TestCase

from fund.models.fund_model import Fund
from fund.models.transaction import FundTransaction


class FundTransactionModelTest(TestCase):

    def setUp(self):
        self.fund = Fund.objects.create()

    def test_valid_income_transaction(self):
        transaction = FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )

        self.assertEqual(transaction.type, "INCOME")
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.after_transaction_balance, 1000)

    def test_valid_expense_transaction_type(self):
        with self.assertRaises(ValidationError):
            FundTransaction.objects.create(
                fund=self.fund,
                type="INVALID",
                amount=1000,
                reason="Test",
                payment_method="Cash",
            )

    def test_zero_amount_is_not_allowed(self):
        with self.assertRaises(ValidationError):
            FundTransaction.objects.create(
                fund=self.fund,
                type="INCOME",
                amount=0,
                reason="Test",
                payment_method="Cash",
            )
            with self.assertRaises(ValidationError):
                transaction = transaction.save()

    def test_expense_cannot_exceed_fund_balance(self):
        FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=500,
            reason="Donation",
            payment_method="cash",
        )

        with self.assertRaises(ValidationError):
            FundTransaction.objects.create(
                fund=self.fund,
                type="EXPENSE",
                amount=600,
                reason="School suplies",
                payment_method="Cash",
            )

    def test_income_updates_after_transaction_balance(self):
        transaction = FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method='Cash',
        )
        self.assertEqual(
            transaction.after_transaction_balance,1000,
        )
    def test_expense_updates_after_transaction_balance(self):
        FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )

        transaction = FundTransaction.objects.create(
            fund=self.fund,
            type="EXPENSE",
            amount=300,
            reason="School supplies",
            payment_method="Cash",
        )

        self.assertEqual(
            transaction.after_transaction_balance,700,
        )

    def test_transaction_string_representation(self):
        transaction = FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )
        self.assertIn("1000Tk",str(transaction))
        self.assertIn("INCOME",str(transaction))
        self.assertIn("1000Tk",str(transaction))