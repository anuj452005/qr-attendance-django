from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    batch = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['student_id']
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if self.user.user_type != 'STUDENT':
            self.user.user_type = 'STUDENT'
            self.user.save()
        super().save(*args, **kwargs)
