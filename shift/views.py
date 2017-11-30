#take request, and send http response 
from django.http import HttpResponse 
from django.template import loader
from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .shift import Shift
from .run import Run
from accounts.forms import UserLoginForm, AdminCreateShiftForm, AdminDeleteShiftForm, AdminCreateRun, signUpForRun
from .shift_group import ShiftGroup
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)
User = get_user_model()

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
	all_runs = Run.objects.all() #database call
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
			html+= "<h2> Mondays 1-4 </h2>"
		if i == 1:
			html+= "<h2> Tuesdays 1-4</h2>"
		if i == 2:
			html+= "<h2> Wednesdays 1-4</h2>"
		if i == 3:
			html+= "<h2> Thursdays 1-4</h2>"
		if i == 4:
			html+= "<h2> Fridays 1-4</h2>"
		html += '<a href="' + urlgroup + '">' + "Grouped Shift #" +str(i) + '</a><br>'
		i = i + 1
	return HttpResponse(html)

def send_command(request, run_id):
	template = loader.get_template('send_command.html')
	context = {}
	form = signUpForRun(request.POST or None)
	context['form'] = form
	http = "test"
	http += '<h1>Sign up for Run</h1> <form method="POST" action='' enctype="multipart/form-data">{% csrf_token %}{{form}}'
	
	if form.is_valid():
		password=form.cleaned_data.get("password")
		user = authenticate(username=request.user.username, password=password)
		if not user.check_password(password):
			raise forms.ValidationError("Incorrect password")
		else:
			print("valid password")
			print(run_id)
			r = Run.objects.get(id=run_id)
			r.user_id = int(request.user.username)
			r.save()
			print(r.user_id)
			print("rendering..")
			render(request, "index.html")
	return render(request, "send_command.html", context)

def detail(request, shift_id):
	template = loader.get_template('details.html')
	shiftobj = Shift.objects.get(id = shift_id);
	html = ''
	html += "<h2>Details for Shift # " + str(shift_id) + "</h2>"
	html += "<h2> Start Time: " + str(shiftobj.start_datetime) + "</h2>"
	html += "<h2> End Time: " + str(shiftobj.end_datetime) + "</h2>"
	html += "<h2> Runs for Shift# " + str(shift_id) + "</h2>"
	i = 0
	for run in shiftobj.runs_related.all():
		html += '<a>' + "Run #" + str(run.id) +" Start Time" + ": " + str(run.start_datetime) + '</a>'
		html += "<br>"
		html += '<a>' + "Run #" + str(i) +" End Time" + ": " + str(run.end_datetime) + '</a>'
		html += "<br>"
		url = ''
		url = '/shift/send_command/' + str(run.id) +'/'
		if (int(run.user_id) == 0):
			html += '<a href="' + url + '">' + "Sign up for Run" + '</a>'
		else:
			html += '<a>' + "User on run: " + str(run.user_id) + "</a>"
		html += "<br>"
		html += "<br>"
		html += "<br>"
		i = i + 1
	return HttpResponse(html)

def detail2(request, group_shift_id):
	template = loader.get_template('index.html')
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