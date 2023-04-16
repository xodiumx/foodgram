from django.contrib.admin import ModelAdmin, StackedInline, register

from .models import Ingredient, Recipe, Tag, AmountIngredient


class IngredientInline(StackedInline):
    model = AmountIngredient
    extra = 5
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    """
    """
    list_display = (
        'name',  
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    """
    """
    inlines = (IngredientInline,)
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


@register(AmountIngredient)
class AmountIngredientAdmin(ModelAdmin):
    list_display = (
        'ingredient', 
    )