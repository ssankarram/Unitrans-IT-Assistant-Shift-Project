from django.db import models
from django.db.models import Q
#from shift.run import Run
from django.utils import timezone
from django.utils.timezone import utc, make_aware, get_default_timezone
import datetime

from shift.shift_group import ShiftGroup

class ShiftManager(models.Manager):

    def create_shift(self, start_datetime, end_datetime):
        #run_times_list -> [{start_time=time, end_time=time},{...},{...}]
        start_datetime = models.DateTimeField()
        end_datetime = models.DateTimeField()
        #run_times_list = Run.objects.all()
        shift1 =  Shift(start_datetime = timezone.now(), end_datetime = timezone.now())
        shift1.save()
        #x = ShiftGroup(shift_group_list = Shift.objects.all())
        #Shift.objects.save()


    def group_shifts(self):
        myShifts = []
        list = Shift.objects.all()
        for s in list:
            temp_list = []
            temp_list.append(s.start_datetime.date().weekday()) #able to save day#, shift
            temp_list.append(s.start_datetime.date().weekday()) #able to save day#, shift
            temp_list.append(s)
            myShifts.append(temp_list)

        finalGroupedShiftsDAY = []
        added = 0
        for i in range(7):
            tempList = []
            for shift in myShifts:
                if i == shift[0]: # if 1 == 6, 1 ==6, 1 == 1 , so on 
                    tempList.append(shift)
                    added = 1
            if added == 1: 
                finalGroupedShiftsDAY.append(tempList)
                added = 0

        print("Grouped shifts: where (x,y) corresponds to x = day of the week, y = shift")
        for group in finalGroupedShiftsDAY:
            print(group)

class Shift(models.Model):
    #runs_related
    db_table="shift"
    objects = ShiftManager()

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    #run_times_list = []

    class Meta:
        app_label = "shift"

class GroupShift(models.Model):
    #runs_related
    db_table="shift"
    #objects = ShiftManager()

    group_shift_list = []
    #run_times_list = []

    class Meta:
        app_label = "shift"