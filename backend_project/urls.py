from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Webpages
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login_page'),
    path('music/', views.music_page, name='music_page'),

    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/gestures/', include('gestures.urls')),
    path('api/music/', include('music_control.urls')),
]
