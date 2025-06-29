from django.db import models
from django.contrib.auth.models import AbstractUser
    
class CustomUser(AbstractUser):  # Inherit from AbstractUser
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("student", "Student"),
        ("teacher", "Teacher"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    grade = models.IntegerField()
    section = models.CharField(max_length=1)  
    attendance = models.FloatField()
    final_aggregate = models.FloatField()
    academic_year = models.CharField(max_length=10, default="2025")
    
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_score = models.FloatField()
    homework_score = models.FloatField()
    final_score = models.FloatField()
    aggregate = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.aggregate = (self.test_score + self.homework_score + self.final_score) 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"

class Homework(models.Model):
       title = models.CharField(max_length=255)
       grade = models.IntegerField()
       section= models.CharField(max_length=1)
       subject = models.CharField(max_length=100)
       due_date = models.DateField(null=True, blank=True)
   
       
       def __str__(self):
        return f"{self.title} - {self.class_name}{self.section} ({self.subject})"
    
class Teacher(models.Model):
     
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"

class Leave(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="leaves")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length =10,
        choices=[('pending','Pending'),('approved','Approved'),('declined','Declined')],
        default='pending'
    )

    def __str__(self):
        return self.message[:50]  # Show first 50 chars in admin
    
class DailyRoutine(models.Model):
    grade = models.CharField(max_length=10)
    routine =   models.ImageField(upload_to='daily_routines/')
    
    


# Model to store training metadata and results for subject/grade/section models
class ModelTraining(models.Model):
    date_trained = models.DateTimeField(auto_now_add=True)
    subject_name = models.CharField(max_length=100)
    grade = models.IntegerField()
    section = models.CharField(max_length=1)
    intercept = models.FloatField()
    coefficients = models.JSONField()
    r2_score = models.FloatField()
    model_path = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"Model trained for {self.subject_name} - Grade {self.grade}{self.section} on {self.date_trained.strftime('%Y-%m-%d %H:%M')}"