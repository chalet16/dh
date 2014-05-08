from django.db import models
from django.contrib.auth.models import User
from cl.recipes.models import Recipe
from cl.schedules.models import Crew

# Create your models here.


class Menu(models.Model):
    date = models.DateField()
    servings = models.IntegerField()

    def __unicode__(self):
        return u'Weekly Menu starting %s' % self.date


class Meal(models.Model):
    menu = models.ForeignKey(Menu)
    crew = models.ForeignKey(
        Crew, limit_choices_to={'category__contains': 'cooking'})
    recipes = models.ManyToManyField(Recipe)
    lateplates = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ['crew__day']

    def __unicode__(self):
        return u'%s %s' % (self.menu, self.crew.name)
