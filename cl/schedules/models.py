from django.db import models
from django.contrib.auth.models import User
# Create your models here.

Days = (
  ('Sun','Sunday'),
  ('Mon','Monday'),
  ('Tue','Tuesday'),
  ('Wed','Wednesday'),
  ('Thu','Thursday'),
  ('Fri','Friday'),
  ('Sat','Saturday'),
)

CrewTypes = (
  ('cooking','Cooking'),
  ('cleaning','Cleaning'),
  ('other','Other'),
)

class Crew(models.Model):
  name = models.CharField(max_length=30)
  day = models.CharField(max_length=3, choices=Days)
  people = models.ManyToManyField(User,blank=True)
  servicetime = models.TimeField()
  category = models.CharField(max_length=8, choices=CrewTypes)

  def __unicode__(self):
    return unicode(self.name)

class CleaningSchedule(models.Model):
  date = models.DateField()

  def  __unicode__(self):
     return u'Cleaning Schedule starting %s' % self.date

class CleaningEvent(models.Model):
  name = models.CharField(max_length=30)
  cleaningschedule = models.ForeignKey(CleaningSchedule)
  datetime = models.DateTimeField()
  people = models.ManyToManyField(User)
  info = models.CharField(max_length=120,blank=True)
