from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import utc, make_aware, get_default_timezone
import datetime
#from shift.shift import Shift

#ShiftGroup object will be a list of specific

class ShiftGroupManager(models.Manager):

    def group_shifts(self, shifts):
        myShifts = []
        list = shifts
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
            #i = i + 1
            #mainShiftGroup.list_of_grouped_shifts=group
            #mainShiftGroup.save()
            #mainShiftGroup.shifts_related.create(start_datetime=group[1].start_datetime, end_datetime=group[1].end_datetime)
            #mainShiftGroup = ShiftGroup()
            #mainShiftGroup.save()
            #for shift in group:
                #mainShiftGroup.shifts_related.create(start_datetime = shift[1].start_datetime, end_datetime = shift[1].end_datetime)
            #    mainShiftGroup.list_of_grouped_shifts += (shift)

        #for groupShifts in ShiftGroup.objects.all():
        #    print(groupShifts)

'''
		for group in finalGroupedShiftsDAY:
            self.shift_group_list.all() #change! its from github
        print(shift1)'''
        #x = ShiftGroup(shift_group_list = Shift.objects.all())
        #Shift.objects.save()


class ShiftGroup(models.Model):
    #runs_related
    db_table="shift_group"
    objects = ShiftGroupManager()
    name = ""
    #grouped_shifts = []
    #shiftGroup will be a list of shifts...that each match w one and other
    #shiftGroup = models.ManyToManyField(Shift, null=True, blank=True, related_name="shifts_related")
    #list_of_grouped_shifts = []

    class Meta:
        app_label = "shift"