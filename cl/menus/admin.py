from django.contrib import admin
from cl.menus.models import Menu, Meal


class MealInline(admin.TabularInline):
    model = Meal
    # filter_horizontal=('recipe',)
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    inlines = (MealInline,)

admin.site.register(Menu, MenuAdmin)
