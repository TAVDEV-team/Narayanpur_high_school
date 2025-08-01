from django.db import models
from nphs_school.models import School
# Create your models here.
class FundTransaction(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="transactions")
    amount = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
