from accounts.models import Account
from django.db import models


class GoverningBody(models.Model):
    account = models.ForeignKey(Account)
    designation = models.CharField(max_length=50, choices=(''))
