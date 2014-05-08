from django.contrib import admin
from cl.schedules.models import Crew, CleaningSchedule, CleaningEvent

class CleaningEventInline(admin.TabularInline):
  model=CleaningEvent
  extra=1

class CleaningScheduleAdmin(admin.ModelAdmin):
  inlines=(CleaningEventInline,)

admin.site.register(Crew)
admin.site.register(CleaningSchedule,CleaningScheduleAdmin)
