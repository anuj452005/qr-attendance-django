from django.db import models

# Create your models here.

class Settings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'
    
    def __str__(self):
        return self.key
    
    @classmethod
    def get_value(cls, key, default=None):
        try:
            setting = cls.objects.get(key=key, is_active=True)
            return setting.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_value(cls, key, value, description=None):
        setting, created = cls.objects.update_or_create(
            key=key,
            defaults={
                'value': value,
                'description': description,
                'is_active': True
            }
        )
        return setting
