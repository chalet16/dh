from django.shortcuts import render_to_response
from cl.menus.models import *
from cl.recipes.models import *
from cl.recipes.views import *
from datetime import *
from django.contrib.auth.models import User
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class mealObj:
    def __init__(self, meal):
        self.pk = meal.pk
        self.name = meal.crew.name
        self.recipes = []
        for recipe in meal.recipes.all():
            self.recipes.append(recipe.name)
        self.lateplates = meal.lateplates.all()


class menuObj:
    def __init__(self, menu):
        self.pk = menu.pk
        self.date = menu.date
        self.name = menu.__unicode__()
        mealsQ = Meal.objects.filter(menu__pk__exact=menu.pk)
        self.meals = []
        for meal in mealsQ:
            self.meals.append(mealObj(meal))


class menusObj:
    def __init__(self, reference):
        self.menus = []
        for menu in Menu.objects.filter(date__range=(reference.thisWeek, reference.thisWeek + timedelta(6))):
            self.menus.append(menuObj(menu))


class menu_weeks:
    def __init__(self, reference):
        self.now = datetime.now().date()
        self.now = self.now - timedelta(self.now.isoweekday() % 7)
        self.thisWeek = reference - timedelta(reference.isoweekday() % 7)
        self.prevWeek = self.thisWeek - timedelta(7)
        self.nextWeek = self.thisWeek + timedelta(7)
        self.prevMonth = self.thisWeek - timedelta(28)
        self.nextMonth = self.thisWeek + timedelta(28)


def show_menus(request):
    menudate = menu_weeks(datetime.now().date())
    menus = menusObj(menudate)
    return render_to_response('pages/menus.html', {'menus': menus.menus, 'date': menudate})


def show_menus_other(request, year, month, day):
    menudate = menu_weeks(date(int(year), int(month), int(day)))
    menus = menusObj(menudate)
    return render_to_response('pages/menus.html', {'menus': menus.menus, 'date': menudate})


class shopping_entry2:
    def __init__(self, measure):
        self.measure = measure
        self.amount = 0


class shopping_ing2:
    def __init__(self, name):
        self.name = name
        self.measures = {}

    def add(self, measure, amount):
        try:
            self.measures[measure].amount += amount
        except:
            self.measures[measure] = shopping_entry2(measure)
            self.measures[measure].amount = amount

    def makeObj(self):
        measures = []
        for measure in self.measures.keys():
            measures.append(self.measures[measure])
        self.measures = measures

    def __unicode__(self):
        return unicode(self.name)


class shopping_list2:
    def __init__(self, menu_id):
        menu = Menu.objects.filter(pk__exact=menu_id)[0]
        meals = Meal.objects.filter(menu__exact=menu)
        self.Ingredients = {}
        for meal in meals:
            for recipe in meal.recipes.all():
                ingQ = RecipeIngredient.objects.filter(recipe__exact=recipe)
                for ing in ingQ:
                    if ing.ingredient.name not in self.Ingredients:
                        self.Ingredients[ing.ingredient.name] = shopping_ing2(
                            ing.ingredient.name)
                    amount = Decimal(ing.amount) * Decimal(
                        menu.servings) / Decimal(recipe.servings)
                    self.Ingredients[
                        ing.ingredient.name].add(ing.measure, amount)
        ingredients = []
        keys = self.Ingredients.keys()
        keys.sort(key=string.lower)
        # print keys
        for ingredient in keys:
            self.Ingredients[ingredient].makeObj()
            ingredients.append(self.Ingredients[ingredient])
        self.Ingredients = ingredients


def show_shopping_list(request, menu_id):
    shop = shopping_list2(menu_id)
    menudate = menu_weeks(datetime.now().date())
    return render_to_response('pages/shopping.html', {'ingredients': shop.Ingredients,
                                                      'date':menudate})


def show_meal(request, meal_id):
    recipesQ = Meal.objects.filter(pk__exact=meal_id)[0].recipes.all()
    recipes = []
    for recipe in recipesQ:
        this = recDisplayObj(recipe.pk)
        this.scale(Meal.objects.filter(pk__exact=meal_id)[0].menu.servings)
        recipes.append(this)
    return render_to_response('pages/meal.html', {'recipes': recipes, 'meal_id': meal_id, 'lateplates': Meal.objects.filter(pk__exact=meal_id)[0].lateplates.all()})

@csrf_exempt
def show_lateplates(request, meal_id):
    if "user" not in request.POST:
        return render_to_response('pages/welcome.html')
    if User.objects.filter(email__iexact=request.POST['user']).count == 0:
        return render_to_response('pages/welcome.html')
    meal = Meal.objects.filter(pk__exact=meal_id)[0]
    if request.method == 'POST':
        if 'Add' in request.POST:
            meal.lateplates.add(User.objects.filter(
                first_name__contains=request.POST['Add'])[0])
            meal.save()
        if 'Remove' in request.POST:
            meal.lateplates.remove(User.objects.filter(
                first_name__contains=request.POST['Remove'])[0])
            meal.save()
    currentUsers = meal.lateplates.all().order_by('first_name')
    pks = []
    for currentUser in currentUsers:
        pks.append(currentUser.pk)
    users = User.objects.all(
    ).exclude(pk__in=pks).exclude(username='admin').order_by('first_name')
    return render_to_response('pages/lateplates.html', {'user': request.POST['user'], 'meal_id': meal_id, 'currentUsers': currentUsers, 'users': users, 'pks': pks})

@csrf_exempt
def add_lateplate(request, meal_id):
    if "user" not in request.POST:
        return render_to_response('pages/welcome.html')
    if User.objects.filter(email__iexact=request.POST['user']).count == 0:
        return render_to_response('pages/welcome.html')
    meal = Meal.objects.filter(pk__exact=meal_id)[0]
    if meal.lateplates.filter(email__iexact=request.POST['user']).count() == 0:
        meal.lateplates.add(
            User.objects.filter(email__iexact=request.POST['user'])[0])

    recipesQ = Meal.objects.filter(pk__exact=meal_id)[0].recipes.all()
    recipes = []
    for recipe in recipesQ:
        this = recDisplayObj(recipe.pk)
        this.scale(Meal.objects.filter(pk__exact=meal_id)[0].menu.servings)
        recipes.append(this)
    return render_to_response('pages/meal.html', {'recipes': recipes, 'meal_id': meal_id, 'lateplates': Meal.objects.filter(pk__exact=meal_id)[0].lateplates.all()})


############################   Deprecated Objects ########################
class shopping_entry:
    def __init__(self, measure):
        self.measure = measure
        self.amount = 0


class shopping_ing:
    def __init__(self, name):
        self.name = name
        self.measures = {}

    def add(self, measure, amount):
        try:
            self.measures[measure].amount += amount
        except:
            self.measures[measure] = shopping_entry(measure)
            self.measures[measure].amount = amount

    def makeObj(self):
        measures = []
        for measure in self.measures.keys():
            measures.append(self.measures[measure])
        self.measures = measures

    def __unicode__(self):
        return unicode(self.name)


def cmp_ingredients(ing1, ing2):
    x = ing1.name
    y = ing2.name
    if x < y:
        return -1
    elif x == y:
        return 0
    else:
        return 1


class shopping_list:
    def __init__(self, menu_id):
        menu = Menu.objects.filter(pk__exact=menu_id)[0]
        meals = Meal.objects.filter(menu__exact=menu)
        self.Ingredients = []
        if meals.count() > 0:
            ingredients = RecipeIngredient.objects.filter(
                recipe__in=meals[0].recipes.all())
        if meals.count() > 1:
            for meal in meals[1:]:
                ingredients = ingredients | RecipeIngredient.objects.filter(
                    recipe__in=meal.recipes.all())
        ingredients = ingredients.order_by('ingredient')
        for ingredient in ingredients.values('ingredient').distinct().order_by('ingredient'):  # look through distinct ingredients
            ingredient_id = ingredient['ingredient']
            ingredient_name = Ingredient.objects.filter(
                pk__exact=ingredient_id)[0].name
            ing_temp = shopping_ing(ingredient_name)
            for ing in ingredients.filter(ingredient__exact=ingredient_id):  # here are all uses of one ingredient
                ing_temp.add(ing.measure, ing.amount)
            ing_temp.makeObj()
            self.Ingredients.append(ing_temp)
        self.Ingredients.sort(cmp_ingredients)
