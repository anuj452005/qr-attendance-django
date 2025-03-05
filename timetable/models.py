from django.db import models
from academics.models import Subject
from teachers.models import Teacher

# Create your models here.

class Timetable(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_entries')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='timetable_entries')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    slot = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20)
    batch = models.CharField(max_length=10)
    
    class Meta:
        ordering = ['day', 'start_time']
        unique_together = ['day', 'slot', 'batch']
    
    def __str__(self):
        return f"{self.subject.code} - {self.day} - {self.slot} - {self.batch}"
