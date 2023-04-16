from django.db.models import Count, Q
from django_filters import rest_framework as filter

from recipes.models import Ingredient, Recipe


class IngredientFilter(filter.FilterSet):
    """Фильтрация ингредиента по названию или по части."""
    search_title = ('Name')
    search_description = ('Search ingredient by part of name')

    name = filter.CharFilter(
        field_name='name',
        lookup_expr='istartswith',)
    
    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filter.FilterSet):
    """
    Фильтрация рецептов по:
        - Автору
        - Тэгам
        -
        -
    """
    # TODO: 
    # is_favorited = filter.CharFilter(
    #     field_name='is_favorited',
    #     lookup_expr='lte'
    # )
    # is_in_shopping_cart = filter.CharFilter(
    #     field_name='is_in_shopping_cart',
    #     lookup_expr='icontains'
    # )
    author = filter.NumberFilter(
        field_name='author__id',
    )
    tags = filter.CharFilter(
        method='filter_tags',)

    class Meta:
        model = Recipe
        #'is_favorited', 'is_in_shopping_cart', 
        fields = ('author', 'tags')
    
    
    def filter_tags(self, queryset, name, value):
        """
        Создаем список slug-ов по которым необходима фильтрация.
        К каждому объекту queryset-а анотируем колличество slug-ов в поле tag.
        Фильтруем по tag-ам из запроса и по их количеству.
        """
        tags = value.split('&tags=')
        return queryset.annotate(num_tags=Count(
                'tags__slug', 
                filter=Q(tags__slug__in=tags),
                distinct=True)).filter(num_tags=len(tags), tags__slug__in=tags)
