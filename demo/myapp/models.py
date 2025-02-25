from django.db import models
from django.contrib.auth.models import AbstractUser
    
class CustomUser(AbstractUser):  # Inherit from AbstractUser
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("student", "Student"),
        ("teacher", "Teacher"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)