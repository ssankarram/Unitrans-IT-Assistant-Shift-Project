from django.db import models

from shift.shift import Shift

# shift does not have a person with associated with it, each Run does. 

class RunManager(models.Manager):

    def create_run(self, start_datetime, end_datetime):
        run1 = Run(start_datetime = start_datetime, end_datetime = end_datetime)
        run1.save()
        print(run1.start_datetime)
        return run1

class Run(models.Model):

    db_table="run"
    objects = RunManager()

    shift = models.ForeignKey(Shift, null=True, blank=True, related_name="runs_related")#add smt about null
    user_id = models.IntegerField(default=0, blank=True)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
#filter it such that only ones on that date and time will get affiliated with that shift
    class Meta:
        app_label = "shift"


#displaying shift on browser
#justify the groupings
#from there, work on the feature of 