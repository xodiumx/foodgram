from django.contrib.admin import ModelAdmin, StackedInline, register

from .models import (AmountIngredient, Favorite, Ingredient, Recipe, RecipeTag,
                     ShoppingCart, Tag)


class IngredientInline(StackedInline):
    extra = 5
    model = AmountIngredient
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


class TagInline(StackedInline):
    extra = 2
    model = Tag.recipes.through
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    inlines = (TagInline, IngredientInline,)
    list_display = ('name', 'favorite_count')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'

    def favorite_count(self, obj):
        return obj.favorites.count()


@register(AmountIngredient)
class AmountIngredientAdmin(ModelAdmin):
    list_display = ('ingredient', )


@register(RecipeTag)
class RecipeTagAdmin(ModelAdmin):
    list_display = ('tag', )


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('recipe', 'user')


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('recipe', 'user')
