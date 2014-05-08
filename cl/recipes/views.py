from django.shortcuts import render_to_response
from cl.recipes.models import *
from cl.recipes.forms import Scale_Recipe
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext


class recObj:
    def __init__(self, id, name, category_id):
        self.id = id
        self.name = name
        self.category_id = category_id

    def __unicode__(self):
        return u'recObj: %s. %s (%s)' % (self.id, self.name, self.category_id)


class recType:
    def __init__(self, id, uniCode):
        self.id = id
        self.uniCode = uniCode

    def __unicode__(self):
        return u'recType: %s (%s)' % (self.unicode, self.id)


class recDisplayIng:
    def __init__(self, name, amount, measure):
        self.name = name
        self.amount = amount
        self.measure = measure


class recDisplayObj:
    def __init__(self, id):
        thisRecipe = Recipe.objects.filter(pk__exact=id)[0]
        self.name = thisRecipe.name
        self.category = thisRecipe.category.__unicode__()
        self.servings = unicode(thisRecipe.servings)
        self.directions = thisRecipe.directions
        self.ingredients = []
        for ing in RecipeIngredient.objects.filter(recipe__pk__exact=id).order_by('ingredient'):
            self.ingredients.append(recDisplayIng(name=ing.ingredient.name, amount=unicode(ing.amount), measure=ing.measure.name))

    def scale(self, number):
        for ing in self.ingredients:
            ing.amount = Decimal(
                ing.amount) * Decimal(number) / Decimal(self.servings)
        self.servings = number


class recPageObj:
    def __init__(self):
        self.state = 'showAll'
        self.urlRecType = '-1'
        self.urlRecId = '-1'
        self.recNames = []
        self.doForm = '-1'
        self.scale = 0
        for rec in Recipe.objects.all():
            self.recNames.append(
                recObj(id=rec.pk, name=rec.name, category_id=rec.category.pk))
        self.recTypes = []
        for type in RecipeType.objects.all():
            self.recTypes.append(
                recType(id=type.pk, uniCode=type.__unicode__()))

    def filter(self):
        self.recNames = []
        for rec in Recipe.objects.all():
            if unicode(rec.category.pk) == unicode(self.urlRecType):
                self.recNames.append(recObj(
                    id=rec.pk, name=rec.name, category_id=rec.category.pk))

    def filterByType(self):
        recNames = self.recNames
        for rec in recNames:
            if str(rec.category_id) != str(self.urlRecType):
                self.recNames.remove(rec)

    def dictionary(self):
        if self.urlRecId != '-1':
            self.recDisplay = recDisplayObj(self.urlRecId)
            if self.scale != 0:
                for ing in self.recDisplay.ingredients:
                    ing.amount = Decimal(ing.amount) * Decimal(
                        self.scale) / Decimal(self.recDisplay.servings)
                    # ing.amount = float(ing.amount) * float(self.scale) /
                    # float(self.recDisplay.servings)
                self.recDisplay.servings = self.scale
            self.doForm = '1'
        else:
            self.recDisplay = []
        return {'state': self.state, 'urlRecType': self.urlRecType, 
                'urlRecId': self.urlRecId, 'recDisplay': self.recDisplay, 
                'recipes': self.recNames, 'recipeTypes': self.recTypes, 
                'doForm': self.doForm, 'form': Scale_Recipe()}


def show_recipes(request):
    recPage = recPageObj()
    dct = recPage.dictionary()
    #commented out at stewards will
    
    #paginator = Paginator(dct['recipes'], 25)
    #page = request.GET.get('page')
    #try:
    #    recipes = paginator.page(page)
    #except PageNotAnInteger:
    #    # If page is not an integer, deliver first page.
    #    recipes = paginator.page(1)
    #except EmptyPage:
    #    # If page is out of range (e.g. 9999), deliver last page of results.
    #    recipes = paginator.page(paginator.num_pages)
    #dict['recipes']=recipes
    return render_to_response("pages/rcpes.html", dct)


def show_recipes_type(request, urlRecType):
    recPage = recPageObj()
    recPage.state = 'showType'
    recPage.urlRecType = urlRecType
    recPage.filter()
    return render_to_response("pages/rcpes.html",recPage.dictionary(),
                              context_instance=RequestContext(request))


def show_recipe(request, urlRecType, urlRecId):
    recPage = recPageObj()
    recPage.state = 'showRecipe'
    recPage.urlRecType = urlRecType
    recPage.urlRecId = urlRecId
    recPage.filter()
    if request.method == 'POST':
        form = Scale_Recipe(request.POST)
        if form.is_valid():
            recPage.scale = form.cleaned_data['servings']
    return render_to_response("pages/rcpes.html", recPage.dictionary(),
                              context_instance=RequestContext(request))
