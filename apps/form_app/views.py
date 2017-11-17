from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
from datetime import datetime, date
import bcrypt

def index(request):
	if request.session.get('name') is None:
		request.session['name'] = ""
	return render(request, 'form_app/index.html')

def register(request):
	result = User.objects.validate_register(request.POST)
	if not result[0]:
		errors = []
		for key, value in result[1].iteritems():
			errors.append(value)
		context = {
		'errors': errors
		}
		return render(request, 'form_app/index.html', context)
	else:
		request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
		return redirect('/success')

def login(request):
	result = User.objects.validate_login(request.POST)
	if not result[0]:
		errors = [result[1]]
		context = {
		'errors': errors
		}
		return render(request, 'form_app/index.html', context)
	else:
		request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
		return redirect('/success')

def success(request):
	return render(request, 'form_app/success.html')

