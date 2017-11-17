from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re


EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be more than 1 character"
        elif not postData['first_name'].isalpha():
            errors['first_name'] = "First name should only contain characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be more than 1 character"
        elif not postData['first_name'].isalpha():
            errors['last_name'] = "Last name should only contain characters"
        if len(postData['email']) < 1:
            errors['email'] = "Email should not be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid!"
        if len(postData['pwd']) < 8:
            errors['pwd'] = "Password should be at least 8 characters"
        if len(postData['confirmPwd']) < 8 or postData['pwd']!=postData['confirmPwd']:
            errors['confirmPwd'] = "Password and Confirm Password should match"
        if len(postData['date']) < 1:
            errors['date'] = "Birth Date cannot be blank"
        if errors:
            return (False, errors)
        else:
            hashPwd = bcrypt.hashpw(postData['pwd'].encode('utf-8'), bcrypt.gensalt())
            self.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashPwd, dob=postData['date'])
            return (True, self.get(first_name=postData['first_name']))

    def validate_login(self, postData):
        try:
            user = self.get(email=postData['email'])
        except:
            user = None
        if user and bcrypt.hashpw(postData['pwd'].encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
            return (True, user)
        return(False, "Invalid login. Email or password is incorrect")

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()