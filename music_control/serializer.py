from rest_framework import serializers
from .models import MusicAction
from devices.models import Device

class MusicActionSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())

    class Meta:
        model = MusicAction
        fields = ['device', 'action']
