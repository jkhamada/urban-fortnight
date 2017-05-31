# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re


class UserManager(models.Manager):
    def login(self, username, password):
        theUser = User.userManager.filter(username = username)
        if bcrypt.hashpw(password.encode(), theUser[0].password.encode()) == theUser[0].password:
            return {'theUser': theUser[0]}
        else:
            return {'errors': 'login Unseccessful'}
    def register(self, name, username, password, confirm_password):
        errors = False
        errLog = {'errors': []}
        if len(username) < 3:
            errLog['errors'].append('Enter a valid username')
        if len(User.userManager.filter(username= username)) > 1:
            errors = True
            errLog['errors'].append('username already exists')
        if len(username) < 1:
            errors = True
            errLog['errors'].append('Must enter a username')
        if len(password) < 8:
            errors = True
            errLog['errors'].append('password is too short')
        if password != confirm_password:
            errors = True
            errLog['errors'].append('passwords do not match')
        if errors == True:
            return errLog
        else:
            newUser = User.userManager.create(name=name, username=username, password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
            return {'theUser': newUser}
        return "register"



class User(models.Model):
    """(User description)"""
    name = models.CharField(blank=True, max_length=100)
    username = models.CharField(blank=True, max_length=100)
    password = models.CharField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()
    def toString(self):
        return self.name + " " + self.username + " " + self.password

class TripsManager(models.Manager):
    def tripAdd(self, postData, user_id):
        errors = {}
        today = datetime.today().strftime('%Y-%m-%d')
        if(len(postData['destination']) < 1):
            errors['destination'] = "Please enter Destination"
        if(len(postData['description']) < 1):
            errors['description'] = "Please enter Description"
        if(errors):
            return {'errors': errors}
        user = User.userManager.get(id=user_id)
        destination = postData['destination']
        description = postData['description']
        travel_date_from = postData['travel_date_from']
        travel_date_to = postData['travel_date_to']
        trip =Trips.tripsManager.create(planner=user,destination=destination, description=description, travel_date_from=travel_date_from, travel_date_to=travel_date_to)
        trip.user.add(user)
        return {'trip':trip}

class Trips(models.Model):
    planner = models.ForeignKey(User, related_name='user_trips')
    user = models.ManyToManyField(User,related_name='trips')
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    tripsManager = TripsManager()
    objects=models.Manager()
