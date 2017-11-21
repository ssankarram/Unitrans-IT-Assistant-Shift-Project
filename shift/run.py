from django.db import models

from shift.shift import Shift


class Run(models.Model):

    db_table="run"

    shift = models.ForeignKey(Shift, null=True, blank=True, related_name="runs_related")#add smt about null
    user_id = models.IntegerField(default=0, blank=True)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    class Meta:
        app_label = "shift"