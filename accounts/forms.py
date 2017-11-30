from django import forms
from django.shortcuts import render, HttpResponseRedirect
from shift.shift import Shift, ShiftManager
from shift.shift_group import ShiftGroup, ShiftGroupManager
from shift.run import Run
from datetime import datetime

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)
User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)
	def clean(self):
		username = self.cleaned_data.get("username")
		password= self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username,password=password)
			if not user:
				raise forms.ValidationError("dne")
			if not user.check_password(password):
				raise forms.ValidationError("incorrect pw")
			if not user.is_active:
				raise forms.ValidationError("no longer active")
		return super(UserLoginForm, self).clean()

class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label = "Email Address")
	#email2 = forms.EmailField(label="Confirm Email")
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			#'email2',
			'password'
		]

	def clean_email(self):
		email = self.cleaned_data.get('email')
		#email2 = self.cleaned_data.get('email2')
		print(email)
		#print(email2)
		#if email != email2:
		#	raise forms.ValidationError("Emails must match.")
		return email

class signUpForRun(forms.Form):
	password = forms.CharField(widget = forms.TextInput())

class AdminCreateRun(forms.Form):
	#user_id = forms.IntegerField(required = False,widget=forms.TextInput())
	start_datetime = forms.CharField(required = False,widget=forms.TextInput())
	end_datetime = forms.CharField(required = False,widget=forms.TextInput())

class AdminDeleteRun(forms.Form):
	start_datetime1 = forms.CharField(required = False,widget=forms.TextInput())
	end_datetime1 = forms.CharField(required = False,widget=forms.TextInput())

class AdminDeleteShiftForm(forms.Form):
	delete_id = forms.CharField(required = False,widget=forms.TextInput())

class AdminCreateShiftForm(forms.Form):
	start_year = forms.CharField(required = False, widget=forms.TextInput())
	start_month = forms.CharField(required = False, widget=forms.TextInput())
	start_day = forms.CharField(required = False, widget=forms.TextInput())
	start_time = forms.CharField(required = False, widget=forms.TextInput())

	end_year = forms.CharField(required = False, widget=forms.TextInput())
	end_month = forms.CharField(required = False, widget=forms.TextInput())
	end_day = forms.CharField(required = False, widget=forms.TextInput())
	end_time = forms.CharField(required = False, widget=forms.TextInput())
	class Meta:
		model = Shift
		fields = [
			'start_datetime',
			'end_datetime',
		]
