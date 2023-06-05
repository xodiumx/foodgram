from base64 import b64decode
from collections import OrderedDict

from django.core.files.base import ContentFile
from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from rest_framework.serializers import (ImageField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField)
from users.models import Follow, User

from .services import RecipeSerivce


class IngredientInfoSerializer(ModelSerializer):
    """Сериализация ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(ModelSerializer):
    """Сериализация тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class AmountIngredientSerializer(ModelSerializer):
    """Сериализация ингредиента и связанной таблицы Amount."""
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class AuthorSerializer(ModelSerializer):
    """
    Сериализация пользователей.
    В методе to_representation добавляем информацию о подписке на пользователя.
    """
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')

    def to_representation(self, instance: User) -> OrderedDict:
        data = super().to_representation(instance)
        user = self.context.get('request').user.id
        data['is_subscribed'] = Follow.objects.filter(
            user=user, following=instance).exists()
        return data


class Base64ImageField(ImageField):
    """
    Декодировка картинки из base64.
    - Из исходной строки извлекаем формат и картинку.
    - Записываем картинку в формате 'recipe.<расширение>.
    """
    def to_internal_value(self, data: str) -> str:
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(b64decode(imgstr), name=f'recipe.{ext}')
        return super().to_internal_value(data)


class RecipeSerializer(ModelSerializer):
    """Сериализцаия рецептов для метода GET."""
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = AmountIngredientSerializer(
        read_only=True, many=True, source='amountingredient_set')
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time',)

    def get_is_favorited(self, obj: Recipe) -> Favorite:
        return RecipeSerivce.get_favorite(self, obj)

    def get_is_in_shopping_cart(self, obj: Recipe) -> ShoppingCart:
        return RecipeSerivce.get_shopping_cart(self, obj)


class RecipeCreateSerializer(ModelSerializer):
    """Сериализцаия рецептов для методов POST и UPDATE."""
    image = Base64ImageField(required=True, allow_empty_file=False)
    ingredients = AmountIngredientSerializer(
        read_only=True, many=True, source='amountingredient_set')
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(),
                                  required=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time',)

    def validate(self, data: OrderedDict) -> OrderedDict:
        return RecipeSerivce.validate_recipe(self, data)

    def create(self, validated_data: dict) -> Recipe:
        return RecipeSerivce.create_recipe(self, validated_data)

    def update(self, instance: Recipe, validated_data: dict) -> Recipe:
        return RecipeSerivce.update_recipe(self, instance, validated_data)


class RecipeShortSerializer(ModelSerializer):
    """Краткая информация о рецепте."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def to_representation(self, instance: Recipe) -> OrderedDict:
        data = super().to_representation(instance)
        request = self.context.get('request')
        data['image'] = f'{request.get_host()}{instance.image.url}'
        return data
