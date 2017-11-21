#take request, and send http response 
from django.http import HttpResponse 
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .shift import Shift
from .forms import UserForm

def index2(request):
	all_shifts = Shift.objects.all() #database call
	template = loader.get_template('shift/index2.html')
	html = ''
	for shift in all_shifts:
		url = '/shift/groups' + '/'
		#html += 'test'
	return HttpResponse(html)

def index(request):
	all_shifts = Shift.objects.all() #database call
	template = loader.get_template('shift/index.html')
	html = ''
	for shift in all_shifts:
		url = '/shift/' + str(shift.id) + '/'
		html += '<a href="' + url + '">' + "Shift #" +str(shift.id) + '</a><br>'
	return HttpResponse(html)

def detail(request, shift_id):
	shiftobj = Shift.objects.get(id = shift_id);
	html = ''
	html += "<h2>Details for Shift # " + str(shift_id) + "</h2>"
	html += "<h2> Start Time: " + str(shiftobj.start_datetime) + "</h2>"
	html += "<h2> End Time: " + str(shiftobj.end_datetime) + "</h2>"
	html += "<h2> Runs for Shift# " + str(shift_id) + "</h2>"
	#html += str(shiftobj.Runs)
	return HttpResponse(html)


class UserFormView(View):
	form_class = UserForm
	tempalte_name = 'shift/registration_form.html'
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('shift:index')