# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Trips
from .models import User
import time
import random
import string

def index(request):

    return render(request, 'belt_app/index.html')

def register(request):
    if(request.method == "POST"):
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        answer = User.userManager.register(name, username, password, confirm_password)
        if answer.has_key('errors'):
            print(answer['errors'])
            return HttpResponse(answer['errors'])
        else:
            return redirect('/')
    else:
        return redirect('/')

def login(request):
    if(request.method == "POST"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        answer = User.userManager.login(username, password)
        if(answer.has_key('errors')):
            return HttpResponse(answer['errors'])
        else:
            theUser = answer['theUser']
            request.session['user'] = theUser.name
            request.session['id'] = theUser.id
            return redirect('/home')
    else:
        return redirect('/')

def home(request):

    return render(request, "belt_app/home.html")

def logout(request):
    request.session.clear()
    return redirect('/')

def trip_add(request):
    if request.method == 'POST':
        response=Trips.tripsManager.tripAdd(request.POST, request.session['user_id'])
        if ("trip" in response):
            return render(request, 'belt_app/home.html')
        else:
            for error in response['errors'].values():
                messages.add_message(request, messages.ERROR, error)
    return render(request,'belt_app/home.html')

def destination(request, id):
    context = {
    "trip": Trips.tripsManager.get(id=id)
    }
    return render(request,'belt_app/trip.html', context)

def join (request, id):
    user=User.userManager.get(id=request.session['user_id'])
    trip=Trips.tripsManager.get(id=id)
    user.trips.add(trip)
    return redirect(reverse('travels:index'))
