from django.shortcuts import render_to_response
from cl.schedules.models import *

# Create your views here.

class crewObj:
  def __init__(self,crew):
    self.name = crew.name
    self.people = []
    for person in crew.people.all():
      self.people.append(person.first_name)

class crewsObj:
  def __init__(self):
    crewsQ = Crew.objects.filter(category__exact='cleaning')
    self.crews = []
    for crew in crewsQ:
      self.crews.append(crewObj(crew))

class eventObj:
  def __init__(self, event):
    self.name = event.name
    self.datetime = event.datetime
    self.people = []
    for person in event.people.all():
      self.people.append(person.first_name)
    self.info = event.info

class scheduleObj:
  def __init__(self, schedule):
    self.date = schedule.date
    self.events = []
    eventsQ = CleaningEvent.objects.filter(cleaningschedule__pk__exact=schedule.pk)
    for event in eventsQ:
      self.events.append(eventObj(event))

class schedulesObj:
  def __init__(self):
    self.schedules = []
    for schedule in CleaningSchedule.objects.all():
      self.schedules.append(scheduleObj(schedule))

def show_cleaning(request):
  crews = crewsObj()
  return render_to_response('pages/cleaning.html',{'crews':crews.crews})


def show_events(request):
  schedules = schedulesObj()
  return render_to_response('pages/events.html',{'schedules':schedules.schedules})
