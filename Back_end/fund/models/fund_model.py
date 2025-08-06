from django.db import models
from nphs_school.models import School
from solo.models import SingletonModel


class Fund(SingletonModel):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="funds",
        default=1,
        editable=False,
    )
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
        return f"{str(self.school.name)}'s current balance {self.balance} Tk"
