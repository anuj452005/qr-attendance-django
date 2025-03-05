from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='STUDENT')
    
    class Meta:
        permissions = [
            ("can_manage_users", "Can manage all users"),
            ("can_manage_attendance", "Can manage attendance"),
            ("can_view_reports", "Can view attendance reports"),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_admin(self):
        return self.user_type == 'ADMIN'
    
    @property
    def is_teacher(self):
        return self.user_type == 'TEACHER'
    
    @property
    def is_student(self):
        return self.user_type == 'STUDENT'
