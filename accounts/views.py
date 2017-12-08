from django.shortcuts import render, HttpResponseRedirect
from .forms import UserLoginForm, UserRegisterForm
from django import forms
from shift.shift import Shift, ShiftManager
from shift.shift_group import ShiftGroup, ShiftGroupManager
from django.http import Http404
from shift.run import Run
from datetime import datetime

batch_index=0

# Create your views here.
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)

from .forms import UserLoginForm, AdminCreateShiftForm, AdminDeleteShiftForm, AdminCreateRun, AdminDeleteRun

def login_view(request):
	title="Login"
	print(request.user.is_authenticated())
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username = username, password=password)
		login(request, user)
		print(request.user.is_authenticated())
		#redirect
		if username == "admin":
			return HttpResponseRedirect('/shift/home/')
		return HttpResponseRedirect('/shift/home/')
	return render(request, "form.html", {"form": form, "title": title})

def register_view(request):
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password) #built in method for user model
		user.save()
		return HttpResponseRedirect('/shift/')
		login(request, user)
	context = {
		"form": form,
		"title": title
	}
	return render(request, "form.html", context)

def logout_view(request):
	logout(request)
	render(request, "form.html", {"username": request.user.username})
	return HttpResponseRedirect('/shift/login/')

def options_view(request):
	if request.user.username != "admin":
		raise Http404
	title = "Options"
	form = AdminCreateShiftForm(request.POST or None)
	form_delete = AdminDeleteShiftForm(request.POST or None)
	form_createrun = AdminCreateRun(request.POST or None)
	form_deleterun = AdminDeleteRun(request.POST or None)

	context = {}
	context['create_form'] = form
	context['delete_form'] = form_delete
	context['create_run_form'] = form_createrun
	context['delete_run_form'] = form_deleterun

	if form.is_valid():
		startYear=form.cleaned_data.get("start_year")
		startMonth=form.cleaned_data.get("start_month")
		startDay=form.cleaned_data.get("start_day")
		startTime=form.cleaned_data.get("start_time")
		
		endYear =form.cleaned_data.get("end_year")
		endMonth=form.cleaned_data.get("end_month")
		endDay=form.cleaned_data.get("end_day")
		endTime=form.cleaned_data.get("end_time")

		global batch_index
		if (startYear):
			cr_date=datetime(int(startYear), int(startMonth), int(startDay), int(startTime))
			cr_date2= datetime(int(endYear), int(endMonth), int(endDay), int(endTime))
			Shift.objects.create_shift(start_datetime=cr_date, end_datetime=cr_date2, run_times_list=Run.objects.all())
			render(request, "index.html")

		print("successfully made shift")
	else:
		print("boo")

	if form_delete.is_valid():
		id_=form_delete.cleaned_data.get("delete_id")
		if (id_):
			print(id_)
			Shift.objects.get(id=int(id_)).delete()
			print("Successfully deleted shift")
			render(request, "index.html")

	if form_createrun.is_valid():
		start_datetime=form_createrun.cleaned_data.get("start_datetime")
		end_datetime=form_createrun.cleaned_data.get("end_datetime")

		bool_ = 0
		for run in Run.objects.all():
			x = str((run.start_datetime))
			y = str((run.end_datetime))
			if (start_datetime == x[:-9] and end_datetime == y[:-9]):
				bool_ = 1
				raise forms.ValidationError("Error: Attempt to make a Run duplicate.")

		if (bool_ == 0 and start_datetime):
			Run.objects.create_run(start_datetime=start_datetime, end_datetime=end_datetime)
			Shift.objects.updateShifts(Run.objects.all())
			print("rendering..")
			render(request, "index.html")

	if form_deleterun.is_valid():
		start_datetime1 = form_deleterun.cleaned_data.get("start_datetime1")
		end_datetime1 = form_deleterun.cleaned_data.get("end_datetime1")
		if (start_datetime1):
			for r in Run.objects.all():
				x = str(start_datetime1)
				y = str(end_datetime1)
				print(x + " " + start_datetime1)
				print(y + " " + end_datetime1)
				if (x == start_datetime1 and y == end_datetime1):
					print("deleting object")
					r.delete()
	else:
		print("boo nothing")
	return render(request, "options.html", context)
	#return HttpResponseRedirect('/options/')
