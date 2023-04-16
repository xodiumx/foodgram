from re import match

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import (
    CharField, EmailField, ModelSerializer,
    Serializer, SlugRelatedField, 
    CurrentUserDefault, Field, SerializerMethodField)

from users.models import User, Follow
from recipes.models import Tag, Ingredient, Recipe, AmountIngredient


class IngredientInfoSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class AmountIngredientSerializer(ModelSerializer):

    class Meta:
        model = AmountIngredient
        fields = ('amount',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        amount = data.pop('amount')
        data['id'] = instance.ingredient.id
        data['name'] = instance.ingredient.name
        data['measurement_unit'] = instance.ingredient.measurement_unit
        data['amount'] = amount
        return data


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


class RecipeSerializer(ModelSerializer):

    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'description', 
                  'cooking_time',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    
    def get_ingredients(self, recipe_obj):
        ingredients = recipe_obj.ingredients.through.objects.filter(
            recipe_id=recipe_obj.id
            ).prefetch_related('ingredient')
        return AmountIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        return None
    
    def get_is_in_shopping_cart(self, obj):
        return None


class RecipeCreateSerializer(ModelSerializer):
    ...