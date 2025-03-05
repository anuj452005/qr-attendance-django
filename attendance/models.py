from django.db import models
from django.utils import timezone
from students.models import Student
from timetable.models import Timetable
from teachers.models import Teacher
import uuid
from accounts.models import CustomUser

# Create your models here.

class QRCode(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='qr_codes')
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"QR Code for {self.timetable} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Default expiration time is 5 minutes from creation
            self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='attendances')
    qr_code = models.ForeignKey(QRCode, on_delete=models.SET_NULL, null=True, related_name='attendances')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(auto_now_add=True)
    is_present = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    device_info = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'timetable', 'date']
        ordering = ['-date', '-time']
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student} - {self.timetable} - {self.date} - {status}"

class AttendanceToken(models.Model):
    token = models.CharField(max_length=64, unique=True)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        return not self.is_used and not self.is_expired()
    
    def __str__(self):
        return f"Token for {self.timetable} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def generate_token(cls, timetable, teacher, expiry_minutes=10):
        token = uuid.uuid4().hex
        expires_at = timezone.now() + timezone.timedelta(minutes=expiry_minutes)
        return cls.objects.create(
            token=token,
            timetable=timetable,
            expires_at=expires_at,
            created_by=teacher
        )
