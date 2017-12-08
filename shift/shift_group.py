from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import utc, make_aware, get_default_timezone
import datetime

class ShiftGroupManager(models.Manager):
    def group_shifts(self, shifts):
        myShifts = []
        list = shifts
        for s in list:
            temp_list = []
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

		#print("Grouped shifts: where (x,y) corresponds to x = day of the week, y = shift")
        for group in finalGroupedShiftsDAY: 
            print("hi")
            mainShiftGroup = ShiftGroup()
            mainShiftGroup.save()
            wholegroup=[]
            for shift in group:
                wholegroup.append(shift[1])
            print(wholegroup)
            mainShiftGroup.shifts_related.set(wholegroup)

class ShiftGroup(models.Model):
    #runs_related
    db_table="shift_group"
    objects = ShiftGroupManager()
    #grouped_shifts = []
    #shiftGroup will be a list of shifts...that each match w one and other
    #shiftGroup = models.ManyToManyField(Shift, null=True, blank=True, related_name="shifts_related")
    #list_of_grouped_shifts = []

    class Meta:
        app_label = "shift"