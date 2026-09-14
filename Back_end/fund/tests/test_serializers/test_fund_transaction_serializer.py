from django.test import TestCase

from fund.models import Fund, FundTransaction
from fund.serializers import FundTransactionSerializer


class FundTransactionSerializerTest(TestCase):

    def setUp(self):
        self.fund = Fund.get_solo()

    def test_serializer_has_expected_fields(self):
        serializer = FundTransactionSerializer()

        expected_fields = [
            "id",
            "type",
            "amount",
            "reason",
            "payment_method",
            "after_transaction_balance",
            "date",
            "created_at",
        ]

        self.assertEqual(
            list(serializer.fields.keys()),
            expected_fields,
        )

    def test_after_transaction_balance_is_read_only(self):
        serializer = FundTransactionSerializer()

        self.assertTrue(
            serializer.fields["after_transaction_balance"].read_only
        )

    def test_valid_income_transaction(self):
        data = {
            "type": "INCOME",
            "amount": 1000,
            "reason": "Donation",
            "payment_method": "Cash",
        }

        serializer = FundTransactionSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_valid_expense_transaction(self):
        FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=5000,
            reason="Donation",
            payment_method="Cash",
        )

        data = {
            "type": "EXPENSE",
            "amount": 2000,
            "reason": "Stationery",
            "payment_method": "Cash",
        }

        serializer = FundTransactionSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_zero_amount_is_invalid(self):
        data = {
            "type": "INCOME",
            "amount": 0,
            "reason": "Invalid transaction",
            "payment_method": "Cash",
        }

        serializer = FundTransactionSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("amount", serializer.errors)

    def test_negative_amount_is_invalid(self):
        data = {
            "type": "INCOME",
            "amount": -100,
            "reason": "Invalid transaction",
            "payment_method": "Cash",
        }

        serializer = FundTransactionSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("amount", serializer.errors)

    def test_amount_greater_than_100_million_is_invalid(self):
        data = {
            "type": "INCOME",
            "amount": 100000001,
            "reason": "Invalid transaction",
            "payment_method": "Cash",
        }

        serializer = FundTransactionSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("amount", serializer.errors)

    def test_invalid_transaction_type(self):
        data = {
            "type": "INVALID",
            "amount": 1000,
            "reason": "Invalid transaction",
            "payment_method": "Cash",
        }

        serializer = FundTransactionSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("type", serializer.errors)

    def test_expense_greater_than_balance_is_invalid(self):
        FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )

        data = {
            "type": "EXPENSE",
            "amount": 1500,
            "reason": "Purchase",
            "payment_method": "Cash",
        }

        serializer = FundTransactionSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("non_field_errors", serializer.errors)

    def test_expense_equal_to_balance_is_valid(self):
        FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )

        data = {
            "type": "EXPENSE",
            "amount": 1000,
            "reason": "Purchase",
            "payment_method": "Cash",
        }

        serializer = FundTransactionSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )