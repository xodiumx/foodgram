from django.db.models import Count, Q
from django_filters import rest_framework as filter

from recipes.models import Ingredient, Recipe, ShoppingCart, Favorite


class IngredientFilter(filter.FilterSet):
    """Фильтрация ингредиента по названию или по части названия."""
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
        - Избранным рецептам
        - Рецептам в корзине
    """
    is_favorited = filter.BooleanFilter(
        method='filter_is_favorited',)
    is_in_shopping_cart = filter.BooleanFilter(
        method='filter_is_in_shopping_cart',)
    author = filter.NumberFilter(field_name='author__id',)
    tags = filter.CharFilter(method='filter_tags',)

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart', )
    
    
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


    def filter_is_favorited(self, queryset, name, value):
        """Фильтруем по id рецепта привязанного к пользователю."""
        user = self.request.user
        if not user.is_anonymous and value:
            ids = [qs.recipe.id for qs in Favorite.objects.filter(
                   user=user)]
            return queryset.filter(id__in=ids)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Фильтруем по id рецепта привязанного к пользователю."""
        user = self.request.user
        if not user.is_anonymous and value:
            ids = [qs.recipe.id for qs in ShoppingCart.objects.filter(
                   user=user)]
            return queryset.filter(id__in=ids)
        return queryset