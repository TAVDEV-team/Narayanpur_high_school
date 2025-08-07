from django.db import models
from solo.models import SingletonModel


class Fund(SingletonModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def balance(self):
        income = (
            self.transactions.filter(type="INCOME").aggregate(
                models.Sum("amount")
            )["amount__sum"]
            or 0
        )

        expense = (
            self.transactions.filter(type="EXPENSE").aggregate(
                models.Sum("amount")
            )["amount__sum"]
            or 0
        )

        return income - expense

    def __str__(self):
        return f"Current balance: {self.balance} Tk"
