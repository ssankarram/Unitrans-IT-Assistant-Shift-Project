from django.conf.urls import url
from django.contrib.auth.views import login
from . import views 

urlpatterns = [
	#/shift
	url(r'^$', views.index, name='index'), #default home page, go to views and look for function called index
	#url(r'(test)^$', views.index, name='index'), #default home page, go to views and look for function called index
	#url(r'^(groups)/$', views.index2, name='index2'),
	#url(r'^login/$', login, {'template_name': 'accounts/login.html'})
	#/register
	#url(r'^register/$', views.UserFormView.as_view(), name='register'), #default home page, go to views and look for function called index

	#/shift/
	url(r'^(?P<shift_id>[0-9]+)/$', views.detail, name="detail"),
]
