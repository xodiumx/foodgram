from django_filters import rest_framework as filter

from recipes.models import Ingredient


class IngredientFilter(filter.FilterSet):

    search_title = ('Name')
    search_description = ('Search ingredient by part of name')

    name = filter.CharFilter(
        field_name='name',
        lookup_expr='istartswith',)
    
    class Meta:
        model = Ingredient
        fields = ('name',)