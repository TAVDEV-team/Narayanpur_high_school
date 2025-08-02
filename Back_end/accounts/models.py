# from django.db import models
# from django.contrib.auth.models import User

# CLASS_CHOICES = [(str(i), str(i)) for i in range(6, 11)]
# SECTION_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C')]
# SUBJECT_CHOICES = [(sub, sub.title()) for sub in ['bangla', 'english', 'math']]
# RELIGION_CHOICES = [(rel, rel.title()) for rel in ['islam', 'hindu', 'buddist', 'chirstian']]
# GROUP_CHOICES = [ (grp, grp.title()) for grp in ['science', 'commerce', 'arts']]
# OPTIONAL_SUBJECT_LIST = [ (grp, grp.title()) for grp in ['science', 'commerce', 'arts']]




# class Account(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     school = models.ForeignKey('School',on_delete=models.CASCADE)
#     mobile = models.CharField(max_length=11)
#     image = models.ImageField(upload_to='Accounts/', null=True, blank=True)
#     religion = models.CharField(max_length=10, choices=RELIGION_CHOICES )
#     joining_date = models.DateField()
#     address = models.TextField()
#     last_education = models.TextField()
#     last_educational_institute = models.CharField(max_length=120)
#     is_active = models.BooleanField(default=True)
#     starting_date = models.DateField()
    
#     def __str__(self):
#         return f"{self.user.username}"



# class Teachers(Account):
#     base_subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
#     is_head_teacher = models.BooleanField(default=False)
#     class_teacer = models.BooleanField(default=False)
#     class_teacher_of = models.ForeignKey('AClass',on_delete=models.SET_NULL)



# class Student(Account):
#     """
#     Represents a student enrolled in the institution.

#     Stores basic profile data (name, gender, phone), 
#     along with foreign key references to class section and year. 
#     Designed to support academic tracking and administrative queries.

#     Fields:
#         - name (str): Full name of the student.
#         - class_section (ClassSection): Class and section assignment.
#         - roll number (int): unique roll number for each student of a class
#         - gender (str): Gender of the student (e.g., Male, Female).
#         - image (img): Photo of the student. 
#         - group (str): if the student is in class (9,10), they must have a group
#         - admission_date (date): When the student was first admitted
#         - religion (str): Religion of the student.
#         - phone (str): Contact number of the student.
#         - year (Year): Academic year the student is enrolled in.
    
#     Usage:
#         student = Student.objects.get(pk=1)
#         print(student.name)

#     Constraints:
#         - Each student must belong to one class section and year.
#         - Phone number is optional.
#     """
#     batch = models.ForeignKey("Batch",on_delete=models.CASCADE)
#     captain_of = models.ForeignKey('Batch',on_delete=models.SET_NULL)
#     roll_number = models.CharField(max_length=10, unique=True,null=True,blank=True)
#     image = models.ImageField(upload_to='students/', null=True, blank=True)
#     group = models.CharField(max_length=10,choices=GROUP_CHOICES)
#     address = models.TextField()
#     optional_subject = models.CharField(max_length=12, choices= OPTIONAL_SUBJECT_LIST)


#     def __str__(self):
#         return f"{self.name} (Class {self.s_class}-{self.section})"
