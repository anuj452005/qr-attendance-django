from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['teacher_id']
    
    def __str__(self):
        return f"{self.teacher_id} - {self.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if self.user.user_type != 'TEACHER':
            self.user.user_type = 'TEACHER'
            self.user.save()
        super().save(*args, **kwargs)
