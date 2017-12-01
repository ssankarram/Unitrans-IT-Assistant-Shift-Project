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

def index4(request):
	i = 0
	template = loader.get_template('index.html')
	html = ""
	html += '<font size="5">'
	html += '<h1> <center>Shifts by Day </h1>'
	for group_shift in ShiftGroup.objects.all():
		urlgroup = '/shift/' + str(group_shift.id) + '/group/'
		html += '<font size="4">'
		if i == 0:
			html+= "<h2><center> Mondays: "
		if i == 1:
			html+= "<h2><center> Tuesdays: "
		if i == 2:
			html+= "<h2><center> Wednesdays: "
		if i == 3:
			html+= "<h2><center> Thursdays: "
		if i == 4:
			html+= "<h2><center> Fridays: "
		html += '</h2><center><a href="' + urlgroup + '">' + "View Shifts" + '</a><br>'
		i = i + 1
	return HttpResponse(html)

def index3(request):
	#i = 1
	template = loader.get_template('index.html')
	html = ""
	html += '<font size="5"><h1><center> Shifts </h1>'
	for shift in Shift.objects.all():
		url = '/shift/' + str(shift.id) + '/'
		if shift.start_datetime.date().weekday() == 0:
			html += '<center><font size="4"><a href="' + url + '">' + "Monday:" + '</a>'
			html += '<a> ' + str(shift.start_datetime.time().hour) + " - " + str(shift.end_datetime.time().hour) + " PM" + '</a><br>'
		
		if shift.start_datetime.date().weekday() == 1:
			html += '<center><font size="4"><a href="' + url + '">' + "Tuesday:" + '</a>'
			html += '<a> ' + str(shift.start_datetime.time().hour) + " - " + str(shift.end_datetime.time().hour) + " PM" + '</a><br>'

		if shift.start_datetime.date().weekday() == 2:
			html += '<center><font size="4"><a href="' + url + '">' + "Wednesday:" + '</a>'
			html += '<a> ' + str(shift.start_datetime.time().hour) + " - " + str(shift.end_datetime.time().hour) + " PM" + '</a><br>'

		if shift.start_datetime.date().weekday() == 3:
			html += '<center><font size="4"><a href="' + url + '">' + "Thursday:" + '</a>'
			html += '<a> ' + str(shift.start_datetime.time().hour) + " - " + str(shift.end_datetime.time().hour) + " PM" + '</a><br>'

		if shift.start_datetime.date().weekday() == 4:
			html += '<center><font size="4"><a href="' + url + '">' + "Friday:" + '</a>'
			html += '<a> ' + str(shift.start_datetime.time().hour) + " - " + str(shift.end_datetime.time().hour) + " PM" + '</a><br>'
	return HttpResponse(html)


def index(request):
	all_shifts = Shift.objects.all() #database call
	all_runs = Run.objects.all() #database call
	template = loader.get_template('index.html')
	html = '<h2><font size="8"><center>Welcome ' + str(request.user.username) + "!</h2>"
	html += "<center><img src='https://farm8.static.flickr.com/7352/12006048986_b8881cefa6_b.jpg' style='width:1350px;height:400px;' alt='W3Schools.com'><br>"
	html += "<font size='5'><center>View shifts and sign up for available runs using UNI.<br><br>"

	url_ = ''
	i = 0
	url_ = '/shift/shift'
	html += '</h2><a href="' + url_ + '">' + "View All Shifts" + '</a><br>'
	url_ = '/shift/groups'
	html += '</h2><a href="' + url_ + '">' + "View All Grouped Shifts" + '</a><br>'
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
	html = '<center>'
	html += "<h2><font size='6'>" + "Details for Shift # " + str(shift_id) + "</h2>"
	html += "<h2><font size='4'> Start Time: " + str(shiftobj.start_datetime) + "</h2>"
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
			if (request.user.username != "admin"):
				html += '<a href="' + url + '">' + "Sign up for Run" + '</a>'
			else:
				url = '/shift/options'
				html += '<a href="' + url + '">' + "Admin, create/edit/view runs via OPTIONS tab." + '</a>'
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

	htmlList = [None] * 12
	j = 0
	added = 0
	templist = []
	
	while j < 8:
		templist = []
		for shift in shiftgroupobj.shifts_related.all():
			if str(shift.start_datetime.time().hour) == str(j):
				templist.append(shift)
		htmlList[j]=(templist)
		j = j + 1

	hournum = 1
	test = 0
	added = 0
	for group in htmlList:
		print(hournum)
		if group != None:
			for shift in group:
				if (shift != None and test == 0):
					html += '<h2><font size="7"><center>' + "Shifts from " + str(hournum) + "-" + " " + str(hournum + 3) + '</h2>'
					test = 1
					added = 1
				html += '<h2><font size="5"><center>' + str(shift.start_datetime) + '</h2>'
				for run in shift.runs_related.all():
					html += '<a><center>' + "Run #" + str(i) +" Start Time" + ": " + str(run.start_datetime) + '</a>'
					html += "<br>"
					html += '<a><center>' + "Run #" + str(i) +" End Time" + ": " + str(run.end_datetime) + '</a>'
					html += "<br>"
					html += '<center><button type="button">Sign up for Run</button>'
					html += "<br>"
					html += "<br>"
		if added == 1:
			hournum = hournum + 3
			added = 0
		test = 0
	return HttpResponse(html)