from django.db import models
import string

# Create your models here.


class Measure(models.Model):
    name = models.CharField(max_length=5)

    def __unicode__(self):
        return unicode(self.name)


class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    form = models.CharField(max_length=30, blank=True)
    category = models.CharField(max_length=30)

    def __unicode__(self):
        if self.form != "":
            return u'%s: %s (%s)' % (self.name, self.form, self.category)
        else:
            return u'%s (%s)' % (self.name, self.category)

    class Meta:
        ordering = ['name', 'form', 'category']


class RecipeType(models.Model):
    category1 = models.CharField(max_length=30)
    category2 = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        if self.category2 == "":
            return unicode(self.category1)
        else:
            return u'%s (%s)' % (self.category1, self.category2)


class Recipe(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(RecipeType)
    directions = models.TextField()
    servings = models.IntegerField()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name']


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    recipe = models.ForeignKey(Recipe)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    measure = models.ForeignKey(Measure)
    special = models.CharField(max_length=60, blank=True)

    def __unicode__(self):
        return u'%s in %s' % (self.ingredient, self.recipe)

#  class Meta:
#    order_with_respect_to = 'ingredient'
