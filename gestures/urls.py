from django.urls import path
from . import views

urlpatterns = [
    path("update/", views.update_gesture, name="update_gesture"),
    path("get/", views.get_gesture, name="get_gesture"),
]