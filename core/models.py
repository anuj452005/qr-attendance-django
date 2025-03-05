from django.db import models
from django.utils import timezone

# Create your models here.

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('ATTENDANCE', 'Attendance'),
        ('OTHER', 'Other'),
    )
    
    user = models.CharField(max_length=150)  # Username
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.CharField(max_length=50, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

class Notification(models.Model):
    recipient = models.CharField(max_length=150)  # Username
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient} - {self.title} - {self.created_at}"
