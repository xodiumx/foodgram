import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import (
    ModelSerializer, PrimaryKeyRelatedField, ImageField, ReadOnlyField, 
    SerializerMethodField, )

from users.models import User, Follow
from recipes.models import (
    Tag, Ingredient, Recipe, AmountIngredient, Favorite, ShoppingCart,)
from .exceptions import UserIsNotAuth


class IngredientInfoSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class AmountIngredientSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context.get('request').user.id
        data['is_subscribed'] = Follow.objects.filter(
            user=user, following=instance).exists()
        return data


class Base64ImageField(ImageField):
    
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name=f'recipe.{ext}')
        return super().to_internal_value(data)


class RecipeSerializer(ModelSerializer):

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

    def get_is_favorited(self, recipe_obj):
        return Favorite.objects.filter(
            user_id=self.context.get('request').user.id,
            recipe=recipe_obj).exists()
    
    def get_is_in_shopping_cart(self, recipe_obj):
        return ShoppingCart.objects.filter(
            user_id=self.context.get('request').user.id,
            recipe=recipe_obj).exists()


class RecipeCreateSerializer(ModelSerializer):

    image = Base64ImageField(required=True, allow_empty_file=False)
    ingredients = AmountIngredientSerializer(
        read_only=True, many=True, source='amountingredient_set')
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), 
                                  required=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 
                  'cooking_time',)


    def validate(self, data):
        if self.context.get('request').user.is_anonymous:
            raise UserIsNotAuth('Только авторизованные пользователи '
                                'могут создавать и обновлять контент')
        ingredients = self.initial_data.get('ingredients')
        data['ingredients'] = ingredients
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient_data in ingredients_data:
            AmountIngredient.objects.create(
                recipe=recipe, 
                ingredient_id=ingredient_data.pop('id'), 
                amount=ingredient_data.pop('amount'))
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get(
            'text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )

        instance.tags.clear()
        instance.tags.set(validated_data.get('tags'))

        AmountIngredient.objects.filter(recipe=instance).all().delete()
        for ingredient_data in validated_data.get('ingredients'):
            AmountIngredient.objects.create(
                recipe=instance, 
                ingredient_id=ingredient_data.pop('id'), 
                amount=ingredient_data.pop('amount'))
        instance.save()
        return instance


class RecipeShortSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        data['image'] = f'{request.get_host()}{instance.image.url}'
        return data
