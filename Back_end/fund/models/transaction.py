from django.core.exceptions import ValidationError
from django.db import models, transaction

from .fund_model import Fund


class FundTransaction(models.Model):
    TRANSACTION_TYPES = (
        ("INCOME", "Income"),
        ("EXPENSE", "Expense"),
    )

    fund = models.ForeignKey(
        Fund,
        on_delete=models.PROTECT,
        related_name="transactions",
        default=1,
        editable=False,
    )
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    amount = models.PositiveIntegerField(default=0)
    reason = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    after_transaction_balance = models.IntegerField(default=0, editable=False)

    def clean(self):
        if self.type not in dict(self.TRANSACTION_TYPES):
            raise ValidationError("Invalid transaction type.")

        if self.amount <= 0:
            raise ValidationError("Amount must be positive.")

        if self.type == "EXPENSE" and self.amount > self.fund.balance:
            raise ValidationError(
                "Cannot spend more than current fund balance."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        with transaction.atomic():
            current_balance = self.fund.balance
            if self.type == "INCOME":
                self.after_transaction_balance = current_balance + self.amount
            elif self.type == "EXPENSE":
                self.after_transaction_balance = current_balance - self.amount

            super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):

        return f"{self.amount}Tk  method {self.type}\
            after transaction balance {self.after_transaction_balance}Tk"
