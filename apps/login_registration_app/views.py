from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.core.urlresolvers import reverse

def index(request):
    return render(request, 'login_registration_app/index.html')

def register(request):
    if User.objects.validation(request.POST, request):
        errorFlag = True
        return redirect (reverse('success'))
    else:
        errorFlag = False
        return redirect(reverse('index'))

def success(request):
    return render(request, 'login_registration_app/success.html')

def login(request):
    if User.objects.verifyUserLogin(request.POST, request):
        errorFlag = True
        return redirect (reverse('success'))
    else:
        errorFlag = False
        return redirect (reverse('index'))