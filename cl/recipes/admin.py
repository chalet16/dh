from django.contrib import admin
from cl.recipes.models import Measure, Ingredient, Recipe, RecipeType, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_filter = ('category',)
    search_fields = ('name',)
    # filter_horizontal=('',)

admin.site.register(Measure)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeType)
