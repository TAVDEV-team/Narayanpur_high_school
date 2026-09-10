from django.test import TestCase

from fund.models.fund_model import Fund
from fund.models.transaction import FundTransaction


class FundModelTest(TestCase):
    def setUp(self):
        self.fund = Fund.objects.create()

    def test_fund_can_be_created(self):
        """Fund object should be created successfully"""
        self.assertIsNotNone(self.fund.pk)
        self.assertEqual(Fund.objects.count(), 1)

    def test_initial_balance_is_zero(self):
        """A new fund with no transactions should have zero balance"""
        self.assertEqual(self.fund.balance, 0)

    def test_balance_with_income(self):
        """Income trasaction should increase the fund balance"""
        FundTransaction.objects.create(
            fund=self.fund,
            type="INCOME",
            amount=1000,
            reason="Donation",
            payment_method="Cash",
        )
        self.assertEqual(self.fund.balance, 1000)

    def test_balance_with_expense(self):
            """Income trasaction should decrease the fund balance"""
            FundTransaction.objects.create(
                fund=self.fund,
                type="INCOME",
                amount=1000,
                reason="Donation",
                payment_method="Cash",
            )
            FundTransaction.objects.create(
                    fund=self.fund,
                    type="EXPENSE",
                    amount=300,
                    reason="School suplies",
                    payment_method="Cash",
            )

            self.assertEqual(self.fund.balance, 700)

    def test_balance_with_multiple_transactions(self):
         """
         Fund balance should equal:
         total income - total expense
         """
         FundTransaction.objects.create(
              fund=self.fund,
              type="INCOME",
              amount=1000,
              reason="Donation",
              payment_method="Cash",
         )
         FundTransaction.objects.create(
              fund=self.fund,
              type="INCOME",
              amount=500,
              reason="Donation",
              payment_method="Bank",
         )
         FundTransaction.objects.create(
              fund=self.fund,
              type="EXPENSE",
              amount=300,
              reason="School supplies",
              payment_method="cash",
         )
         self.assertEqual(self.fund.balance, 1200)

    def test_fund_string_representation(self):
         """Fund __str__ should contain the current balance"""
         self.assertEqual(str(self.fund), "Current balance: 0 Tk")

         FundTransaction.objects.create(
              fund=self.fund,
              type="INCOME",
              amount=1000,
              reason="Donation",
              payment_method="Cash",
         )
         self.assertEqual(str(self.fund),"Current balance: 1000 Tk")
        