from django.db import models


class Syllabus(models.Model):
    title = models.CharField(max_length=255)
    aclass = models.OneToOneField(
        'nphs_school.AClass', null=True, blank=True, on_delete=models.SET_NULL
    )
    file = models.FileField(upload_to="syllabus/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
