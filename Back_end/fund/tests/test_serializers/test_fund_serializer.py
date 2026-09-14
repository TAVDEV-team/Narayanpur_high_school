from django.test import TestCase
from fund.models import Fund, FundTransaction
from fund.serializers.fund_serializer import FundSerializer

class FundSerializerTest(TestCase):
    def setUp(self):
        self.fund = Fund.get_solo()

    def test_fund_serializer_contains_expected_fields(self):
        serializer = FundSerializer(instance=self.fund)

        expected_fields = [
            "id",
            "balance",
            "created_at",
            "updated_at",
        ]

        self.assertEqual(
            list(serializer.fields.keys()),
            expected_fields,
        )

    def test_fund_serializer_returns_initial_balance(self):
        serializer = FundSerializer(instance=self.fund)

        self.assertEqual(
            serializer.data["balance"],
            self.fund.balance,
        )

    def test_fund_serializer_returns_balance_after_income(self):
        FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )

        serializer = FundSerializer(instance=self.fund)

        self.assertEqual(
            serializer.data["balance"],
            1000,
        )
    def test_fund_serializer_returns_balance_after_expense(self):
        FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=5000,
            reason="Donation",
            payment_method="cash",
        )

        FundTransaction.objects.create(
            fund=self.fund,
            type="EXPENSE",
            amount=2000,
            reason="Stationary",
            payment_method="Cash",
        )

        serializer = FundSerializer(instance=self.fund)

        self.assertEqual(
            serializer.data["balance"],
            3000
        )

        def test_balance_is_included_in_serialized_data(self):
            serializer = FundSerializer(instance=self.fund)

            self.assertIn("balance", serializer.data)