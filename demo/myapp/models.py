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
        self.aggregate = (self.test_score + self.homework_score + self.final_score) / 3
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

    def __str__(self):
        return self.message[:50]  # Show first 50 chars in admin
    
    
