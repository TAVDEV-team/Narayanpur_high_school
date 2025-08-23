from django.db import models


class Syllabus(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="syllabus/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
