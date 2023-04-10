from re import match

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import (
    CharField, EmailField, ModelSerializer,
    Serializer, SlugRelatedField, 
    CurrentUserDefault, Field)

from recipes.models import Tag, Ingredient


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)