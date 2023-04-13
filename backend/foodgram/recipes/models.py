from django.db import models

from users.models import User
from foodgram.settings import AMOUNT_CHOICES


class Tag(models.Model):
    """
    Модель тэгов:
    Attributes:
        - name: Название
        - color: Цвет в формате hex
        - slug: Уникальный слаг
    """
    name = models.CharField(
        'Тэг',
        max_length=50,
        null=False,
        blank=False,
        )
    color = models.CharField(
        'Цвет',
        max_length=16,
        null=False,
        blank=False,)
    slug = models.SlugField(
        max_length=16, 
        unique=True,
        null=False,
        blank=False,)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель ингредиентов:
    Attributes:
        - name: Название
        - amount: Количество
        - measurement_unit: Ед. измерения
    """
    name = models.CharField(
        'Ингредиент',
        max_length=120,
        db_index=True,
        null=False,
        blank=False)
    amount = models.IntegerField(
        'Количество',
        default=0,
        choices=AMOUNT_CHOICES)
    measurement_unit = models.CharField(
        'Ед. измерения',
        max_length=20,
        null=False,
        blank=False,)
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель для рецептов.
    Attributes:
        - author: Автор рецепта
        - name: Название
        - image: Картинка
        - description: Описание
        - ingredients: Ингрединты
        - tags: Тэги
        - cooking_time: Время приготовления
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
        'Картинка',
        null=False,
        blank=False
    )
    description = models.TextField(
        'Описание',
        max_length=500,
        null=False,
        blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        related_name='recipes',
        verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name='recipes',
        verbose_name='Тэги')
    cooking_time = models.IntegerField(
        'Время приготовления',
        null=False,
        blank=False
    )
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    # TODO Убрать created сделать по -id
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name