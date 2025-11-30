from django.shortcuts import render
import subprocess
import threading
import os
import sys

def index(request):
    return render(request, 'index.html')

def login_page(request):
    return render(request, 'login.html')

def music_page(request):
    return render(request, "music.html")