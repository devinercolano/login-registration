# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re

emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
passwordCharUppercaseRegEx = re.compile(r'[A-Z]+')
passwordNumRegEx = re.compile(r'[0-9]+')

class UserManager(models.Manager):
    def validation(self, userInformation, request):
        errorFlag = False
        if len(userInformation['firstName']) < 2:
            messages.warning(request, "first name cannot be empty!")
            errorFlag = True
        elif userInformation['firstName'].isalpha() == False :
            messages.warning(request, "First name must contain only alphabetic characters!")
            errorFlag = True
        
        if len(userInformation['lastName']) < 2:
            messages.warning(request, "Last name cannot be empty!", 'error')
            errorFlag = True
        elif userInformation['lastName'].isalpha() == False :
            messages.warning(request, "Last name must contain only alphabetic characters!")
            errorFlag = True

        if len(userInformation['email']) < 1:
            messages.warning(request, "email cannot be empty!")
            errorFlag = True
        elif not emailRegEx.match(userInformation['email']):
            messages.warning(request, "Invalid Email Address!")
            errorFlag = True   

        if len(userInformation['password']) < 1 :
            messages.warning(request, "Password cannot be empty!")
            errorFlag = True
        elif len(userInformation['password']) <= 8:
            messages.warning(request, "Password must be longer than 8 characters")
            errorFlag = True

        if userInformation['password'] != userInformation['confirmPassword'] :
            messages.warning(request, "Password confirmation and password entries must match!")
            errorFlag = True
    
        if not passwordCharUppercaseRegEx.search(userInformation['password']) :
            errorFlag = True
            messages.warning(request, "Password must contain at least 1 uppercase letter")

        if not passwordNumRegEx.search(userInformation['password']) :
            errorFlag = True
            messages.warning(request, "Password must contain at least 1 number")   

        if User.objects.filter(email = userInformation['email']):
                messages.warning(request, "Error! Duplicate email")
                errorFlag = True
        if errorFlag == True :
            messages.success(request, "Success! Welcome" + userInformation['first_name'] + "!")
            hashed = bcrypt.hashpw(userInformation['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name = userInformation['first_name'], last_name = userInformation['last_name'], email = userInformation['email'], password = hashed)

    def verifyUserLogin(self, userInformation, request):
        errorFlag = True
        if User.objects.filter(email=userInformation['email']):
            hashed = User.objects.get(email = userInformation['email']).password
            hashed = hashed.encode('utf-8')
            password = userInformation['password']
            password = password.encode('utf-8')
            if bcrypt.hashpw(password, hashed) == hashed:
                messages.success(request, "Success! Welcome, " + User.objects.get(email = userInformation['email']).first_name + "!")
                errorFlag = True
            else:
                messages.warning(request, "Unsuccessful login. Incorrect password")
                errorFlag = False
        else:
            messages.warning(request, "Unsuccessful login. Your email is incorrect.")
            errorFlag = False
        return errorFlag

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    userManager = UserManager()