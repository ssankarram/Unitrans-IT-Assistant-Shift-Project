#take request, and send http response 
from django.http import HttpResponse 
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .shift import Shift
from .shift_group import ShiftGroup
#from .forms import UserForm

def index2(request):
	all_shifts = Shift.objects.all() #database call
	template = loader.get_template('index2.html')
	html = ''
	for shift in all_shifts:
		url = '/shift/groups' + '/'
		#html += 'test'
	return HttpResponse(html)

def index(request):
	all_shifts = Shift.objects.all() #database call
	template = loader.get_template('index.html')
	html = ''
	i = 1
	html += '<h1> Shifts </h1>'
	for shift in all_shifts:
		url = '/shift/' + str(shift.id) + '/'
		html += '<a href="' + url + '">' + "Shift #" +str(i) + '</a><br>'
		i = i + 1
	#for shift in 
	html += '<br></br>'
	urlgroup = ''
	i = 0
	html += '<h1> Grouped Shifts -- Day </h1>'
	for group_shift in ShiftGroup.objects.all():
		urlgroup = '/shift/' + str(group_shift.id) + '/group/'
		if i == 0:
			html+= "<h2> Monday </h2>"
		if i == 1:
			html+= "<h2> Tuesday </h2>"
		if i == 2:
			html+= "<h2> Wednesday </h2>"
		if i == 3:
			html+= "<h2> Thursday </h2>"
		if i == 4:
			html+= "<h2> Friday </h2>"
		html += '<a href="' + urlgroup + '">' + "Grouped Shift #" +str(i) + '</a><br>'
		i = i + 1
	return HttpResponse(html)

def detail(request, shift_id):
	shiftobj = Shift.objects.get(id = shift_id);
	html = ''
	html += "<h2>Details for Shift # " + str(shift_id) + "</h2>"
	html += "<h2> Start Time: " + str(shiftobj.start_datetime) + "</h2>"
	html += "<h2> End Time: " + str(shiftobj.end_datetime) + "</h2>"
	html += "<h2> Runs for Shift# " + str(shift_id) + "</h2>"
	i = 0
	#html += "Sign Up For Runs"
	for run in shiftobj.runs_related.all():
		html += '<a>' + "Run #" + str(run.id) +" Start Time" + ": " + str(run.start_datetime) + '</a>'
		html += "<br>"
		html += '<a>' + "Run #" + str(i) +" End Time" + ": " + str(run.end_datetime) + '</a>'
		html += "<br>"
		html += '<button type="button">Sign up for Run</button>'
		html += "<br>"
		html += "<br>"
		i = i + 1
	return HttpResponse(html)

def detail2(request, group_shift_id):
	shiftgroupobj = ShiftGroup.objects.get(id = group_shift_id);
	html = ''
	i = 0
	for shift in shiftgroupobj.shifts_related.all():
		html += '<h2>' + "Shift# " + str(i) + ": " + str(shift.start_datetime) + '</h2>'
		for run in shift.runs_related.all():
			html += '<a>' + "Run #" + str(i) +" Start Time" + ": " + str(run.start_datetime) + '</a>'
			html += "<br>"
			html += '<a>' + "Run #" + str(i) +" End Time" + ": " + str(run.end_datetime) + '</a>'
			html += "<br>"
			html += '<button type="button">Sign up for Run</button>'
			html += "<br>"
			html += "<br>"
		i = i + 1
	return HttpResponse(html)