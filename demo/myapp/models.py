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
   
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    grade = models.IntegerField()
    section = models.CharField(max_length=1)  
    attendance = models.FloatField()
    test_score = models.FloatField()
    homework_score = models.FloatField()
    final_exam = models.FloatField()
    aggregate = models.FloatField()
    
