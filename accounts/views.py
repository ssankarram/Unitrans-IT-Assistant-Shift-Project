from django.shortcuts import render, HttpResponseRedirect
from .forms import UserLoginForm, UserRegisterForm
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

from .forms import UserLoginForm, AdminCreateShiftForm, AdminDeleteShiftForm

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
			return HttpResponseRedirect('/shift/options/')
		return HttpResponseRedirect('/shift/')
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
	return render(request, "form.html", {})

def options_view(request):
	if request.user.username != "admin":
		raise Http404
	title = "Options"
	form = AdminCreateShiftForm(request.POST or None)
	form_delete = AdminDeleteShiftForm(request.POST or None)

	context = {}
	context['create_form'] = form
	context['delete_form'] = form_delete
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

	else:
		print("boo nothing")
	return render(request, "options.html", context)
	#return HttpResponseRedirect('/options/')
