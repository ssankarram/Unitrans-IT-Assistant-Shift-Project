from django.db import models

# Create your models here.
'''
class Shift(models.Model):
	#create variables 
	def __str__(self):
		return self.shift_title + "; " + self.shift_time
	shift_title = models.CharField(max_length=30) # Shift1, Shift2, etc
	shift_time = models.CharField(max_length=30)

class Run(models.Model): #associate run with shift
	#run needs to be part of a shift, so to link together 
	shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
	run_time = models.CharField(max_length=30) #11:00-11:05..
	run_description = models.CharField(max_length=30) #description
	'''