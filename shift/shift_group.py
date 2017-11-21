from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import utc, make_aware, get_default_timezone
import datetime
#from shift.shift import Shift

class ShiftGroupManager(models.Manager):
    def check_groupings(list):
    	#list = Shift.objects.all()
    	list
    	#for shift in list:
    		#console.log(shift)

class ShiftGroup(models.Model):
    #runs_related
    db_table="shift_group"
    objects = ShiftGroupManager()

    shift_group_list =[]

    #shiftGroup will be a list of shifts...that each match w one and other

    class Meta:
        app_label = "shift"