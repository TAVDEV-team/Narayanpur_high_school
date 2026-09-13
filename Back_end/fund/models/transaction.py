from datetime import date

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.timezone import now

from .fund_model import Fund
from school_backend.logger import get_logger

logger = get_logger(__name__)


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
    date = models.DateField(default=date.today)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    amount = models.PositiveIntegerField(default=0)
    reason = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=now, editable=False)
    after_transaction_balance = models.IntegerField(default=0, editable=False)

    def clean(self):
        if self.type not in dict(self.TRANSACTION_TYPES):
            logger.warning(f"Invalid transaction type attempted: {self.type}")
            raise ValidationError("Invalid transaction type.")

        if self.amount <= 0:
            logger.warning(
                f"Rejected non-positive transaction amount: {self.amount}"
            )
            raise ValidationError("Amount must be positive.")

        if self.type == "EXPENSE" and self.amount > self.fund.balance:
            logger.warning(
                f"Rejected expense of {self.amount}\
                exceeding balance of {self.fund.balance}"
            )
            raise ValidationError(
                "Cannot spend more than current fund balance."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        with transaction.atomic():
            fund = Fund.objects.select_for_update().get(pk=self.fund_id)
            current_balance = fund.balance
            if self.type == "INCOME":
                self.after_transaction_balance = current_balance + self.amount
            elif self.type == "EXPENSE":
                self.after_transaction_balance = current_balance - self.amount
            logger.info(
                f"Transaction saved: type={self.type} amount={self.amount} "
                f"balance_before={current_balance}\
                 balance_after={self.after_transaction_balance}"
            )
            super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):

        return f"{self.amount}Tk  method {self.type}\
            after transaction balance {self.after_transaction_balance}Tk"
