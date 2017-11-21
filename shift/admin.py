from django.contrib import admin

# Register your models here.

from shift.shift import Shift, ShiftManager
from shift.run import Run

class ChoiceInline(admin.StackedInline):
	model = Run
	extra = 3

class ShiftAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['shift_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Shift, ShiftAdmin)
