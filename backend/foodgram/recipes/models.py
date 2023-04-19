from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from .exceptions import CantSubscribe


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
        upload_to='recipes/',
        null=False,
        blank=False
    )
    text = models.TextField(
        'Описание',
        max_length=500,
        null=False,
        blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=True,
        related_name='recipes',
        verbose_name='Ингредиенты',
        through='AmountIngredient',)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes',
        verbose_name='Тэги',
        through='RecipeTag')
    cooking_time = models.IntegerField(
        'Время приготовления',
        validators=(MaxValueValidator(500), MinValueValidator(1)),
        null=False,
        blank=False
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    """
    Модель для связи количества ингредиентов.
    Attributes:
        - ingredient: FK to Ingredient model
        - recipe: FK to Recipe model
        - amount: integer value
    """
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField(
        'Количество',
        default=1, 
        validators=(MaxValueValidator(500), MinValueValidator(1)),)


class RecipeTag(models.Model):
    """
    Модель для связи рецептов и тегов.
    Attributes:
        - tag: FK to Tag model
        - recipe: FK to Recipe model
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)


class Favorite(models.Model):
    """
    Модель для добавления рецептов в избранное.
    Attributes:
        - user: FK to User model
        - recipe: FK to Recipe model
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_user_favorite',
                violation_error_message='Повторная подписка',
            )
        ]

    def clean(self):
        """Валидация повторной подписки и подписки на свой рецепт."""
        if self.user == self.recipe.author:
            raise CantSubscribe(
                {'detail': 'Нельзя подписаться на свой рецепт'})
        
        if Favorite.objects.filter(
            user=self.user,
            recipe=self.recipe).exists():
            raise CantSubscribe(
                {'detail': 'Нельзя подписаться повторно'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Favorite, self).save(*args, **kwargs)


class ShoppingCart(models.Model):
    """
    Модель для добавления рецептов в корзину.
    Attributes:
        - user: FK to User model
        - recipe: FK to Recipe model
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_user_cart',
                violation_error_message='Повторная добавление в корзину',
            )
        ]

    def clean(self):
        """Валидация повторной подписки и подписки на свой рецепт."""
        if ShoppingCart.objects.filter(
            user=self.user,
            recipe=self.recipe).exists():
            raise CantSubscribe(
                {'detail': 'Рецепт уже в корзине'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ShoppingCart, self).save(*args, **kwargs)