from django.contrib.admin import ModelAdmin, register

from .models import Ingredient, Recipe, Tag


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    """
    """
    list_display = (
        'name',
        'amount',  
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    """
    """
    list_display = (
        'name', 
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@register(Tag)
class TagAdmin(ModelAdmin):
    """
    """
    list_display = (
        'name', 
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'