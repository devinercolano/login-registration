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
    def validation(self, postData):
        response = {}
        messages = {}

        errorFlag = False
        if len(postData['first_name']) < 2:
            messages["first_name"]=("first name cannot be empty!")
            errorFlag = True
        elif postData['first_name'].isalpha() == False :
            messages["first_name"]= ("First name must contain only alphabetic characters!")
            errorFlag = True

        if len(postData['last_name']) < 2:
            messages["last_name"] = ("Last name cannot be empty!", 'error')
            errorFlag = True
        elif postData['last_name'].isalpha() == False :
            messages["last_name"]= ("Last name must contain only alphabetic characters!")
            errorFlag = True

        if len(postData['email']) < 1:
            messages["email"]=("email cannot be empty!")
            errorFlag = True
        elif not emailRegEx.match(postData['email']):
            messages["email"]=("Invalid Email Address!")
            errorFlag = True

        if len(postData['password']) < 1 :
            messages["password"]=("Password cannot be empty!")
            errorFlag = True
        elif len(postData['password']) <= 8:
            messages["password"]=("Password must be longer than 8 characters")
            errorFlag = True

        if postData['password'] != postData['confirmPassword'] :
            messages["password"]=("Password confirmation and password entries must match!")
            errorFlag = True

        if not passwordCharUppercaseRegEx.search(postData['password']) :
            errorFlag = True
            messages["password"]=("Password must contain at least 1 uppercase letter")

        if not passwordNumRegEx.search(postData['password']) :
            errorFlag = True
            messages["password"]=("Password must contain at least 1 number")   

        if User.objects.filter(email = postData['email']):
                messages["email"]=("Error! Duplicate email")
                errorFlag = True
        if errorFlag == False :
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashed)
            response['user']= user
        
        response['message']= messages
        response['errorFlag'] = errorFlag
        
        return response

    def verifyUserLogin(self, postData):
        messages = {}
        response = {}
        errorFlag = False
        email_address = User.objects.filter(email=postData['email'])
        print "email address: ", email_address
        if len(email_address) < 1 :
            messages['login'] = ("Unsuccessful login. Incorrect email")
            errorFlag = True
        else : 
            hashed = User.objects.get(email=postData['email']).password
            if not bcrypt.checkpw(postData['password'].encode(), hashed.encode()):
                messages['login'] = ("Unsuccessful login. Incorrect password")
                errorFlag = True            
        
        if errorFlag == False :
            messages['success'] = ("Welcome" + User.objects.get(email = postData['email']).first_name + "!")
            print "messages in verifyUserLogin: ", messages
        
        response['message']= messages
        response['errorFlag'] = errorFlag

        return response

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    userManager = UserManager()