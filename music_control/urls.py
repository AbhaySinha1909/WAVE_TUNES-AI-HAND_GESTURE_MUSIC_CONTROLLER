from django.urls import path
from .views import MusicControlView

urlpatterns = [
    path('control/', MusicControlView.as_view(), name='music-control'),
]
