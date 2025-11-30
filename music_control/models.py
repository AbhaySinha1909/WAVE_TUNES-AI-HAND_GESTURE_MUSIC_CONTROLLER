from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from devices.models import Device

class MusicAction(models.Model):
    ACTION_CHOICES = [
        ('play', 'Play'),
        ('pause', 'Pause'),
        ('stop', 'Stop'),
        ('next', 'Next Track'),
        ('prev', 'Previous Track'),
        ('volume_up', 'Volume Up'),
        ('volume_down', 'Volume Down'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.device.name} - {self.action}"
