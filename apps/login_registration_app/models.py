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
        errors = {}

        errorFlag = False
        if len(postData['first_name']) < 2:
            errors["first_name"]=("first name cannot be empty!")
            errorFlag = True
        elif postData['first_name'].isalpha() == False :
            errors["first_name"]= ("First name must contain only alphabetic characters!")
            errorFlag = True

        if len(postData['last_name']) < 2:
            errors["last_name"] = ("Last name cannot be empty!", 'error')
            errorFlag = True
        elif postData['last_name'].isalpha() == False :
            errors["last_name"]= ("Last name must contain only alphabetic characters!")
            errorFlag = True

        if len(postData['email']) < 1:
            errors["email"]=("email cannot be empty!")
            errorFlag = True
        elif not emailRegEx.match(postData['email']):
            errors["email"]=("Invalid Email Address!")
            errorFlag = True

        if len(postData['password']) < 1 :
            errors["password"]=("Password cannot be empty!")
            errorFlag = True
        elif len(postData['password']) <= 8:
            errors["password"]=("Password must be longer than 8 characters")
            errorFlag = True

        if postData['password'] != postData['confirmPassword'] :
            errors["password"]=("Password confirmation and password entries must match!")
            errorFlag = True

        if not passwordCharUppercaseRegEx.search(postData['password']) :
            errorFlag = True
            errors["password"]=("Password must contain at least 1 uppercase letter")

        if not passwordNumRegEx.search(postData['password']) :
            errorFlag = True
            errors["password"]=("Password must contain at least 1 number")   

        if User.objects.filter(email = postData['email']):
                errors["email"]=("Error! Duplicate email")
                errorFlag = True
        if errorFlag == False :
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashed)
            response['user']= user
        
        response['error']=errors
        response['errorFlag'] = errorFlag
        
        return response

    def verifyUserLogin(self, postData):
        errors = {}
        response = {}
        errorFlag = False
        email_address = User.objects.filter(email=postData['email'])
        print "email address: ", email_address
        if len(email_address) < 1 :
            errors['login'] = ("Unsuccessful login. Incorrect email")
            errorFlag = True
        else : 
            hashed = User.objects.get(email=postData['email']).password
            if not bcrypt.checkpw(postData['password'].encode(), hashed.encode()):
                errors['login'] = ("Unsuccessful login. Incorrect password")
                errorFlag = True            
        
        if errorFlag == False :
            errors['success'] = ("Welcome" + User.objects.get(email = postData['email']).first_name + "!")
            print "errors in verifyUserLogin: ", errors
        
        response['error']= errors
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