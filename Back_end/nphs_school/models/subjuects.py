from django.db import models

class Subjects(models.Model):
    name_of_subject = models.CharField(max_length=120,unique=True)
    subject_code = models.CharField(max_length=4,unique=True)

    def clean(self):
        
        return super().clean()
    
    def save(self):
        self.full_clean()
        return super().save()
    def __str__(self):
        return f"{self.name_of_subject}-{self.subject_code}"