from django.db import models

from users.models import User


class Tag(models.Model):
    ...


class Ingredient(models.Model):
    ...


class Recipe(models.Model):
    """
    Модель для рецептов.
    Attributes:
        - author: Автор рецепта
        - name:
        - image:
        - description:
        - ingredients:
        - tags:
        - cooking_time:
    """
    author  = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        null=False,
        blank=False
    )
    name = models.CharField(
        'Название рецепта',
        max_length=120,
        db_index=True,
        null=False,
        blank=False
    )
    image = models.ImageField(
        null=False,
        blank=False
    )
    description = models.TextField(
        max_length=500,
        null=False,
        blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
    )
    tags = models.ManyToManyField(
        Tag,
    )
    cooking_time = models.IntegerField(
        null=False,
        blank=False
    )