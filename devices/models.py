# Create your models here.
from django.db import models
from users.models import CustomUser

class Device(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)
    bluetooth_id = models.CharField(max_length=100)
    connected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
