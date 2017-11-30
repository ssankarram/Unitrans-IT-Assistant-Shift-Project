from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import utc, make_aware, get_default_timezone
import datetime

from shift.shift_group import ShiftGroup

class ShiftManager(models.Manager):

    def updateRuns(self, run_times_list_updated2):
        for shift in Shift.objects.all():
            temp=[]
            shift.runs_related.set(temp)
            actualRuns=[]
            for run in run_times_list_updated2:
                if ((run.start_datetime.date() == shift.start_datetime.date()) and (run.start_datetime.time().hour >= shift.start_datetime.hour and run.end_datetime.time().hour <=  shift.end_datetime.hour)):
                    actualRuns.append(run)
            shift.runs_related.set(actualRuns)

    def updateShifts(self, run_times_list_updated):
        for shift in Shift.objects.all():
            temp=[]
            shift.runs_related.set(temp)
            actualRuns=[]
            for run in run_times_list_updated:
                if ((run.start_datetime.date() == shift.start_datetime.date()) and (run.start_datetime.time().hour >= shift.start_datetime.hour and run.end_datetime.time().hour <=  shift.end_datetime.hour)):
                    actualRuns.append(run)
            shift.runs_related.set(actualRuns)

    def create_shift(self, start_datetime, end_datetime, run_times_list):
        shift1 = Shift(start_datetime = start_datetime, end_datetime = end_datetime)
        shift1.save()
        actualRuns=[]
        for run in run_times_list:
            if ((run.start_datetime.date() == shift1.start_datetime.date()) and (run.start_datetime.time().hour >= shift1.start_datetime.hour and run.end_datetime.time().hour <=  shift1.end_datetime.hour)):
                actualRuns.append(run)
        shift1.runs_related.set(actualRuns)
        return shift1

    def group_shifts(self):
        myShifts = []
        list = Shift.objects.all()
        for s in list:
            temp_list = []
            temp_list.append(s.start_datetime.date().weekday()) #able to save day#, shift
            #fix where its justify 
            #valuable on both fronts: group based on day + timing 
                #employer can see who's accoutnable for missing a certain time slot 
                #asking when emplohyee is not free (bc bigger set) 
            #temp_list.append(s.start_datetime.date().hour()) #able to save day#, shift
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
            #initialize finalgroupsshiftsday as a groupshift
            #forieng key related to the shift itself 

        #print(Shift.objects.get(id=5).start_datetime.date())
        #next, display grouped shifts underneath the shift list 
        #form in browser (to enter dates)

        #make_aware 
        #get_default_timezone

class Shift(models.Model):
    #runs_related
    db_table="shift"
    objects = ShiftManager()
 
    shiftGroup = models.ForeignKey(ShiftGroup, null=True, blank=True, related_name="shifts_related")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    #run_times_list = []

    class Meta:
        app_label = "shift"
