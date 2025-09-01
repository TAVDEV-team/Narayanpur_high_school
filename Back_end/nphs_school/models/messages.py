from django.db import models

# from


class Messages(models.Model):
    message_of = models.ForeignKey(
        "accounts.TeacherAccount", on_delete=models.CASCADE
    )
    message = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message_of} {self.created_at}"
