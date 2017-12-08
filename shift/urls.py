from django.conf.urls import url
from django.contrib.auth.views import login
from . import views 
from .views import send_command
from accounts.views import (login_view, logout_view, register_view, options_view)

urlpatterns = [
	#/shift
	url(r'^$', views.index, name='index'), #default home page, go to views and look for function called index
	#url(r'(test)^$', views.index, name='index'), #default home page, go to views and look for function called index
	#url(r'^(groups)/$', views.index2, name='index2'),
	#url(r'^login/$', login, {'template_name': 'accounts/login.html'})
	#/register
	#url(r'^register/$', views.UserFormView.as_view(), name='register'), #default home page, go to views and look for function called index

	#/shift/,...
	url(r'^home/', views.index, name='index1'),
	url(r'^shift/', views.index3, name='index3'),
	url(r'^groups/', views.index4, name='index3'),
	url(r'^(?P<shift_id>[0-9]+)/$', views.detail, name="detail"),
	url(r'^send_command/(?P<run_id>[0-9]+)', views.send_command, name='send_command'),
	url(r'^(?P<group_shift_id>[0-9]+)/group/$', views.detail2, name="detail2"),
	url(r'^unassign/(?P<run_id>[0-9]+)', views.unassign, name='unassign'),
	url(r'^delete/(?P<run_id>[0-9]+)/(?P<shift_id>[0-9]+)', views.deleterun, name='deleterun'),
	url(r'^edit/(?P<run_id>[0-9]+)/(?P<shift_id>[0-9]+)', views.editrun, name='editrun'),
	url(r'^login/', login_view, name='login'),
	url(r'^logout/', logout_view, name='logout'),
	url(r'^register/', register_view, name='register'),
	url(r'^options/', options_view, name="options"),
]